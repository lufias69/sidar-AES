"""
Analyze experiment results vs gold standard to calibrate prompting strategies.
"""
import json
import os
from pathlib import Path
from typing import Dict, List, Tuple
import statistics

class CalibrationAnalyzer:
    def __init__(self, gold_dir: str, experiment_dir: str):
        self.gold_dir = Path(gold_dir)
        self.experiment_dir = Path(experiment_dir)
        self.grade_values = {
            'A': 4.0,
            'B': 3.0,
            'C': 2.0,
            'D/E': 1.0,
            'D': 1.0,
            'E': 0.0
        }
        
    def load_gold_standard(self) -> Dict:
        """Load all gold standard results."""
        gold_data = {}
        for file in self.gold_dir.glob("*.json"):
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                student_name = data['student_name']
                gold_data[student_name] = data
        return gold_data
    
    def load_experiment_results(self, trial: int = 1) -> Dict:
        """Load experiment results for a specific trial."""
        exp_data = {}
        trial_dir = self.experiment_dir / f"trial_{trial}"
        if not trial_dir.exists():
            return exp_data
            
        for file in trial_dir.glob("*.json"):
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                student_name = data['student_name']
                exp_data[student_name] = data
        return exp_data
    
    def compare_grades(self, gold_grade: str, exp_grade: str) -> int:
        """Compare two grades and return difference in levels."""
        gold_val = self.grade_values.get(gold_grade, 0)
        exp_val = self.grade_values.get(exp_grade, 0)
        return gold_val - exp_val
    
    def analyze_student(self, gold: Dict, exp: Dict) -> Dict:
        """Analyze differences for one student."""
        results = {
            'student_name': gold['student_name'],
            'total_score_diff': 0,
            'questions': [],
            'criteria_diffs': {
                'Pemahaman Konten': [],
                'Organisasi & Struktur': [],
                'Argumen & Bukti': [],
                'Gaya Bahasa & Mekanik': []
            }
        }
        
        # Match questions by content
        for gold_q in gold['questions']:
            # Find matching question in experiment
            exp_q = None
            for eq in exp['questions']:
                if eq['question'] == gold_q['question']:
                    exp_q = eq
                    break
            
            if not exp_q:
                continue
            
            # Compare weighted scores
            gold_score = gold_q['weighted_score']
            exp_score = exp_q['weighted_score']
            score_diff = gold_score - exp_score
            results['total_score_diff'] += score_diff
            
            # Compare individual criteria
            q_analysis = {
                'question': gold_q['question'][:80] + '...',
                'gold_score': gold_score,
                'exp_score': exp_score,
                'score_diff': score_diff,
                'criteria': {}
            }
            
            for criterion in results['criteria_diffs'].keys():
                gold_grade = gold_q['grades'].get(criterion, 'D/E')
                exp_grade = exp_q['grades'].get(criterion, 'D/E')
                diff = self.compare_grades(gold_grade, exp_grade)
                
                q_analysis['criteria'][criterion] = {
                    'gold': gold_grade,
                    'exp': exp_grade,
                    'diff': diff
                }
                
                results['criteria_diffs'][criterion].append(diff)
            
            results['questions'].append(q_analysis)
        
        return results
    
    def analyze_all(self, trial: int = 1) -> Dict:
        """Analyze all students."""
        gold_data = self.load_gold_standard()
        exp_data = self.load_experiment_results(trial)
        
        all_results = {
            'students': [],
            'overall': {
                'total_students': 0,
                'avg_score_diff': 0,
                'criteria_stats': {}
            }
        }
        
        total_diff = 0
        criteria_all_diffs = {
            'Pemahaman Konten': [],
            'Organisasi & Struktur': [],
            'Argumen & Bukti': [],
            'Gaya Bahasa & Mekanik': []
        }
        
        for student_name, gold in gold_data.items():
            if student_name not in exp_data:
                continue
            
            exp = exp_data[student_name]
            student_result = self.analyze_student(gold, exp)
            all_results['students'].append(student_result)
            
            total_diff += student_result['total_score_diff']
            
            for criterion, diffs in student_result['criteria_diffs'].items():
                criteria_all_diffs[criterion].extend(diffs)
        
        all_results['overall']['total_students'] = len(all_results['students'])
        if all_results['students']:
            all_results['overall']['avg_score_diff'] = total_diff / len(all_results['students'])
        
        # Calculate criteria statistics
        for criterion, diffs in criteria_all_diffs.items():
            if diffs:
                all_results['overall']['criteria_stats'][criterion] = {
                    'avg_diff': statistics.mean(diffs),
                    'std_dev': statistics.stdev(diffs) if len(diffs) > 1 else 0,
                    'undergrading_count': sum(1 for d in diffs if d > 0),
                    'overgrading_count': sum(1 for d in diffs if d < 0),
                    'exact_match': sum(1 for d in diffs if d == 0),
                    'total': len(diffs)
                }
        
        return all_results
    
    def print_report(self, results: Dict):
        """Print detailed analysis report."""
        print("\n" + "="*80)
        print("CALIBRATION ANALYSIS REPORT")
        print("="*80)
        
        overall = results['overall']
        print(f"\nTotal Students Analyzed: {overall['total_students']}")
        print(f"Average Score Difference: {overall['avg_score_diff']:.3f}")
        print("  (Positive = Gold Standard higher, Negative = Experiment higher)")
        
        print("\n" + "-"*80)
        print("CRITERIA ANALYSIS")
        print("-"*80)
        
        for criterion, stats in overall['criteria_stats'].items():
            print(f"\n{criterion}:")
            print(f"  Average Difference: {stats['avg_diff']:.3f} grade levels")
            print(f"  Std Deviation: {stats['std_dev']:.3f}")
            print(f"  Undergrading (AI too harsh): {stats['undergrading_count']}/{stats['total']} ({stats['undergrading_count']/stats['total']*100:.1f}%)")
            print(f"  Overgrading (AI too lenient): {stats['overgrading_count']}/{stats['total']} ({stats['overgrading_count']/stats['total']*100:.1f}%)")
            print(f"  Exact Match: {stats['exact_match']}/{stats['total']} ({stats['exact_match']/stats['total']*100:.1f}%)")
        
        # Find worst cases
        print("\n" + "-"*80)
        print("WORST UNDERGRADING CASES (AI too harsh)")
        print("-"*80)
        
        worst_cases = []
        for student in results['students']:
            for q in student['questions']:
                if q['score_diff'] > 0.5:  # Gold standard > 0.5 points higher
                    worst_cases.append({
                        'student': student['student_name'],
                        'question': q['question'],
                        'diff': q['score_diff'],
                        'gold': q['gold_score'],
                        'exp': q['exp_score'],
                        'criteria': q['criteria']
                    })
        
        worst_cases.sort(key=lambda x: x['diff'], reverse=True)
        
        for i, case in enumerate(worst_cases[:5], 1):
            print(f"\n{i}. {case['student']} - Diff: {case['diff']:.2f}")
            print(f"   Question: {case['question']}")
            print(f"   Gold: {case['gold']:.2f}, Exp: {case['exp']:.2f}")
            print(f"   Criteria issues:")
            for crit, vals in case['criteria'].items():
                if vals['diff'] > 0:
                    print(f"     - {crit}: {vals['gold']} → {vals['exp']} (diff: {vals['diff']:.1f})")
        
        print("\n" + "="*80)
        print("RECOMMENDATIONS")
        print("="*80)
        
        # Generate recommendations based on analysis
        recs = []
        
        for criterion, stats in overall['criteria_stats'].items():
            if stats['avg_diff'] > 0.3:  # Significant undergrading
                recs.append(f"✓ {criterion}: AI is TOO HARSH (avg diff: {stats['avg_diff']:.2f})")
                recs.append(f"  → Consider using 'lenient' strategy or adjust rubric wording")
            elif stats['avg_diff'] < -0.3:  # Significant overgrading
                recs.append(f"✓ {criterion}: AI is TOO LENIENT (avg diff: {stats['avg_diff']:.2f})")
                recs.append(f"  → Consider using 'strict' strategy or clarify rubric standards")
            else:
                recs.append(f"✓ {criterion}: Well calibrated (avg diff: {stats['avg_diff']:.2f})")
        
        if overall['avg_score_diff'] > 0.5:
            recs.append(f"\n✓ OVERALL: AI is significantly harsher than gold standard")
            recs.append(f"  → Recommend testing 'lenient' or 'few-shot' strategies")
            recs.append(f"  → Or adjust baseline rubric descriptions to be more generous")
        elif overall['avg_score_diff'] < -0.5:
            recs.append(f"\n✓ OVERALL: AI is significantly more lenient than gold standard")
            recs.append(f"  → Recommend testing 'strict' or 'detailed-rubric' strategies")
        else:
            recs.append(f"\n✓ OVERALL: Good alignment with gold standard")
        
        for rec in recs:
            print(rec)
        
        print("\n" + "="*80)
    
    def save_report(self, results: Dict, output_file: str):
        """Save analysis results to JSON."""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\nDetailed results saved to: {output_file}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Analyze and calibrate grading strategies')
    parser.add_argument('--experiment', default='test_01',
                        help='Experiment ID to analyze')
    parser.add_argument('--trial', type=int, default=1,
                        help='Trial number to analyze')
    parser.add_argument('--gold-dir', default='results/gold_standard',
                        help='Directory containing gold standard files')
    parser.add_argument('--output', default=None,
                        help='Output JSON file for detailed results')
    
    args = parser.parse_args()
    
    # Construct experiment directory path
    exp_dir = f"results/experiments/{args.experiment}"
    
    if not os.path.exists(args.gold_dir):
        print(f"Error: Gold standard directory not found: {args.gold_dir}")
        return
    
    if not os.path.exists(exp_dir):
        print(f"Error: Experiment directory not found: {exp_dir}")
        return
    
    analyzer = CalibrationAnalyzer(args.gold_dir, exp_dir)
    results = analyzer.analyze_all(args.trial)
    analyzer.print_report(results)
    
    if args.output:
        analyzer.save_report(results, args.output)
    else:
        # Default output location
        output_file = f"results/calibration_{args.experiment}_trial{args.trial}.json"
        analyzer.save_report(results, output_file)


if __name__ == "__main__":
    main()
