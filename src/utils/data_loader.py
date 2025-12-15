"""
Data Loader Utility
Load and process student answers, questions, and lecturer scores
"""

import pandas as pd
import json
from pathlib import Path
from typing import Dict, List, Optional, Any


class DataLoader:
    """Load and manage essay data"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.raw_dir = self.data_dir / "raw"
        self.processed_dir = self.data_dir / "processed"
        
        # Create directories if they don't exist
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)
    
    def load_questions(self, file_path: Optional[str] = None) -> pd.DataFrame:
        """
        Load essay questions
        
        Expected format:
        question_id, question_text, topic, difficulty
        
        Args:
            file_path: Path to questions file (CSV or JSON)
            
        Returns:
            DataFrame with questions
        """
        if file_path is None:
            file_path = self.raw_dir / "questions.csv"
        else:
            file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Questions file not found: {file_path}")
        
        if file_path.suffix == '.csv':
            df = pd.read_csv(file_path)
        elif file_path.suffix == '.json':
            df = pd.read_json(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")
        
        # Validate required columns
        required_cols = ['question_id', 'question_text']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        return df
    
    def load_student_answers(self, file_path: Optional[str] = None) -> pd.DataFrame:
        """
        Load student essay answers
        
        Expected format:
        student_id, question_id, answer_text
        
        Args:
            file_path: Path to answers file (CSV or JSON)
            
        Returns:
            DataFrame with answers
        """
        if file_path is None:
            file_path = self.raw_dir / "student_answers.csv"
        else:
            file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Answers file not found: {file_path}")
        
        if file_path.suffix == '.csv':
            df = pd.read_csv(file_path)
        elif file_path.suffix == '.json':
            df = pd.read_json(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")
        
        # Validate required columns
        required_cols = ['student_id', 'question_id', 'answer_text']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        return df
    
    def load_lecturer_scores(self, file_path: Optional[str] = None) -> pd.DataFrame:
        """
        Load lecturer ground truth scores
        
        Expected format:
        student_id, question_id, criterion_name, grade, score
        OR
        student_id, question_id, overall_score, [criterion1_grade, criterion2_grade, ...]
        
        Args:
            file_path: Path to lecturer scores file (CSV or JSON)
            
        Returns:
            DataFrame with lecturer scores
        """
        if file_path is None:
            file_path = self.raw_dir / "lecturer_scores.csv"
        else:
            file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Lecturer scores file not found: {file_path}")
        
        if file_path.suffix == '.csv':
            df = pd.read_csv(file_path)
        elif file_path.suffix == '.json':
            df = pd.read_json(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")
        
        # Validate required columns
        required_cols = ['student_id', 'question_id']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        return df
    
    def create_unified_dataset(
        self,
        questions_df: pd.DataFrame,
        answers_df: pd.DataFrame,
        lecturer_scores_df: Optional[pd.DataFrame] = None
    ) -> List[Dict[str, Any]]:
        """
        Create unified dataset combining questions, answers, and scores
        
        Args:
            questions_df: Questions DataFrame
            answers_df: Student answers DataFrame
            lecturer_scores_df: Optional lecturer scores DataFrame
            
        Returns:
            List of dictionaries with complete essay data
        """
        # Merge questions and answers
        merged = answers_df.merge(
            questions_df,
            on='question_id',
            how='left'
        )
        
        # Add lecturer scores if provided
        if lecturer_scores_df is not None:
            merged = merged.merge(
                lecturer_scores_df,
                on=['student_id', 'question_id'],
                how='left'
            )
        
        # Convert to list of dicts
        dataset = []
        for _, row in merged.iterrows():
            essay_data = {
                'student_id': str(row['student_id']),
                'question_id': str(row['question_id']),
                'question': row['question_text'],
                'answer': row['answer_text']
            }
            
            # Add lecturer scores if available
            if lecturer_scores_df is not None:
                lecturer_data = {}
                for col in lecturer_scores_df.columns:
                    if col not in ['student_id', 'question_id'] and col in row:
                        lecturer_data[col] = row[col]
                if lecturer_data:
                    essay_data['lecturer_scores'] = lecturer_data
            
            dataset.append(essay_data)
        
        return dataset
    
    def save_unified_dataset(self, dataset: List[Dict[str, Any]], filename: str = "unified_dataset.json"):
        """Save unified dataset to processed directory"""
        output_path = self.processed_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(dataset, f, ensure_ascii=False, indent=2)
        print(f"Saved unified dataset to: {output_path}")
        return output_path
    
    def load_unified_dataset(self, filename: str = "unified_dataset.json") -> List[Dict[str, Any]]:
        """Load unified dataset from processed directory"""
        input_path = self.processed_dir / filename
        if not input_path.exists():
            raise FileNotFoundError(f"Unified dataset not found: {input_path}")
        
        with open(input_path, 'r', encoding='utf-8') as f:
            dataset = json.load(f)
        
        print(f"Loaded {len(dataset)} essays from: {input_path}")
        return dataset
    
    def create_example_data(self):
        """Create example data files for testing"""
        # Example questions
        questions = pd.DataFrame({
            'question_id': [f'Q{i}' for i in range(1, 9)],
            'question_text': [
                'Jelaskan konsep Automated Essay Scoring (AES) dan implikasinya untuk pendidikan.',
                'Diskusikan kelebihan dan kekurangan penggunaan AI dalam penilaian esai.',
                'Bagaimana bias dalam algoritma AI dapat mempengaruhi penilaian esai?',
                'Jelaskan peran machine learning dalam sistem AES modern.',
                'Apa saja tantangan etis dalam implementasi AES di institusi pendidikan?',
                'Bandingkan pendekatan berbasis aturan vs machine learning dalam AES.',
                'Bagaimana AES dapat membantu meningkatkan kualitas pembelajaran siswa?',
                'Diskusikan masa depan AES dalam konteks pendidikan digital.'
            ],
            'topic': ['AES Basics'] * 8,
            'difficulty': ['Medium'] * 8
        })
        
        # Example student answers (minimal, users should replace with real data)
        answers_data = []
        for student_num in range(1, 11):  # 10 students
            for q_num in range(1, 9):  # 8 questions
                answers_data.append({
                    'student_id': f'S{student_num:03d}',
                    'question_id': f'Q{q_num}',
                    'answer_text': f'[Placeholder answer from student {student_num} for question {q_num}. Replace with real student essay.]'
                })
        
        answers = pd.DataFrame(answers_data)
        
        # Save example files
        questions.to_csv(self.raw_dir / 'example_questions.csv', index=False)
        answers.to_csv(self.raw_dir / 'example_student_answers.csv', index=False)
        
        print(f"Created example data files in: {self.raw_dir}")
        print("- example_questions.csv (8 questions)")
        print("- example_student_answers.csv (80 placeholder answers)")
        print("\nReplace placeholder answers with real student essays!")


# Example usage
if __name__ == "__main__":
    loader = DataLoader()
    
    # Create example data
    print("Creating example data files...")
    loader.create_example_data()
    
    print("\nExample data structure:")
    print("="*60)
    
    # Try loading (will use examples)
    try:
        questions = loader.load_questions("data/raw/example_questions.csv")
        print(f"\nQuestions loaded: {len(questions)}")
        print(questions.head())
        
        answers = loader.load_student_answers("data/raw/example_student_answers.csv")
        print(f"\nAnswers loaded: {len(answers)}")
        print(answers.head())
        
        # Create unified dataset
        dataset = loader.create_unified_dataset(questions, answers)
        print(f"\nUnified dataset created: {len(dataset)} essays")
        print("\nSample essay:")
        print(json.dumps(dataset[0], indent=2, ensure_ascii=False))
        
    except FileNotFoundError as e:
        print(f"File not found: {e}")
