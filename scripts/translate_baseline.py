"""
Translate Baseline Results to Indonesian

Translates all English justification and overall_comment fields
in baseline JSON files to Indonesian using Google Translate API.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any
from deep_translator import GoogleTranslator
import time
from tqdm import tqdm

def translate_text(text: str, src: str = 'en', dest: str = 'id') -> str:
    """
    Translate text using Google Translate.
    
    Args:
        text: Text to translate
        src: Source language (default: English)
        dest: Destination language (default: Indonesian)
    
    Returns:
        Translated text
    """
    if not text or text.strip() == "":
        return text
    
    try:
        translator = GoogleTranslator(source=src, target=dest)
        # Split long text into chunks (Google Translate has 5000 char limit)
        max_length = 4500
        if len(text) <= max_length:
            return translator.translate(text)
        
        # Split by sentences for long text
        sentences = text.split('. ')
        translated = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) < max_length:
                current_chunk += sentence + ". "
            else:
                if current_chunk:
                    translated.append(translator.translate(current_chunk.strip()))
                current_chunk = sentence + ". "
        
        if current_chunk:
            translated.append(translator.translate(current_chunk.strip()))
        
        return " ".join(translated)
    
    except Exception as e:
        print(f"Translation error: {e}")
        return text


def translate_grading_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Translate justification and overall_comment in grading result.
    
    Args:
        result: Grading result dict (ChatGPT or Gemini)
    
    Returns:
        Translated grading result
    """
    if 'error' in result:
        return result
    
    # Translate scores justifications
    if 'scores' in result:
        for criterion, data in result['scores'].items():
            if 'justification' in data:
                original = data['justification']
                translated = translate_text(original)
                data['justification'] = translated
                print(f"    ✓ {criterion}: {len(original)} → {len(translated)} chars")
    
    # Translate overall comment
    if 'overall_comment' in result and result['overall_comment']:
        original = result['overall_comment']
        translated = translate_text(original)
        result['overall_comment'] = translated
        print(f"    ✓ Overall comment: {len(original)} → {len(translated)} chars")
    
    return result


def translate_student_file(file_path: Path) -> None:
    """
    Translate all grading results in a student file.
    
    Args:
        file_path: Path to student JSON file
    """
    print(f"\n{'='*80}")
    print(f"Processing: {file_path.name}")
    print('='*80)
    
    # Load file
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    student_name = data.get('student_name', 'Unknown')
    total_questions = len(data.get('questions', []))
    
    print(f"Student: {student_name}")
    print(f"Questions: {total_questions}")
    
    # Process each question
    for i, question_data in enumerate(data['questions'], 1):
        print(f"\nQuestion {i}/{total_questions}:")
        
        # Translate ChatGPT results
        if 'chatgpt' in question_data:
            print("  ChatGPT:")
            question_data['chatgpt'] = translate_grading_result(question_data['chatgpt'])
            time.sleep(0.5)  # Rate limiting
        
        # Translate Gemini results
        if 'gemini' in question_data:
            print("  Gemini:")
            question_data['gemini'] = translate_grading_result(question_data['gemini'])
            time.sleep(0.5)  # Rate limiting
    
    # Save translated file
    output_path = file_path.parent / f"{file_path.stem}_id.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Saved: {output_path}")
    
    # Backup original
    backup_path = file_path.parent / "backup_english" / file_path.name
    backup_path.parent.mkdir(exist_ok=True)
    with open(backup_path, 'w', encoding='utf-8') as f:
        # Re-read original
        with open(file_path, 'r', encoding='utf-8') as orig:
            f.write(orig.read())
    print(f"📦 Backup: {backup_path}")


def main():
    """Main entry point."""
    baseline_dir = Path("results/baseline_batch")
    
    if not baseline_dir.exists():
        print(f"❌ Directory not found: {baseline_dir}")
        return 1
    
    # Find all student files
    student_files = sorted(baseline_dir.glob("student_*.json"))
    
    if not student_files:
        print(f"❌ No student files found in {baseline_dir}")
        return 1
    
    print(f"Found {len(student_files)} student files to translate")
    print(f"Total translations: {len(student_files)} students × 7 questions × 2 models × 5 fields = ~{len(student_files) * 70} translations")
    print("\nThis will take approximately 5-10 minutes...")
    
    confirm = input("\nProceed? (y/n): ")
    if confirm.lower() != 'y':
        print("Cancelled.")
        return 0
    
    # Process each file
    for file_path in tqdm(student_files, desc="Translating files"):
        try:
            translate_student_file(file_path)
        except Exception as e:
            print(f"\n❌ Error processing {file_path.name}: {e}")
            continue
    
    print("\n" + "="*80)
    print("TRANSLATION COMPLETE!")
    print("="*80)
    print(f"Translated: {len(student_files)} files")
    print(f"Output: results/baseline_batch/*_id.json")
    print(f"Backup: results/baseline_batch/backup_english/")
    print("\nNext steps:")
    print("  1. Review translated files (*_id.json)")
    print("  2. Replace original files if satisfied")
    print("  3. Update prompt system for Indonesian default")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
