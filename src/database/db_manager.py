"""
Database Manager for AES Grading System

Provides checkpoint and resume functionality using SQLite.
Stores all grading results to prevent data loss and enable progress tracking.
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any, Tuple


class DatabaseManager:
    """Manages SQLite database for grading results with checkpoint/resume support."""
    
    def __init__(self, db_path: str = "results/grading_results.db"):
        """
        Initialize database manager.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._create_tables()
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection with JSON support."""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn
    
    def _create_tables(self):
        """Create database tables if they don't exist."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS grading_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                experiment_id TEXT NOT NULL,
                trial_number INTEGER NOT NULL,
                student_id TEXT NOT NULL,
                student_name TEXT NOT NULL,
                question_number INTEGER NOT NULL,
                question_text TEXT NOT NULL,
                answer_text TEXT NOT NULL,
                model TEXT NOT NULL,
                strategy TEXT NOT NULL,
                grades TEXT,
                weighted_score REAL,
                justification TEXT,
                overall_comment TEXT,
                tokens_used INTEGER,
                api_call_time REAL,
                timestamp DATETIME NOT NULL,
                status TEXT NOT NULL,
                error_message TEXT,
                UNIQUE(experiment_id, trial_number, student_id, question_number)
            )
        """)
        
        # Create index for faster queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_experiment_trial 
            ON grading_results(experiment_id, trial_number)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_status 
            ON grading_results(status)
        """)
        
        conn.commit()
        conn.close()
    
    def insert_or_update(
        self,
        experiment_id: str,
        trial_number: int,
        student_id: str,
        student_name: str,
        question_number: int,
        question_text: str,
        answer_text: str,
        model: str,
        strategy: str,
        status: str = "pending",
        grades: Optional[Dict[str, str]] = None,
        weighted_score: Optional[float] = None,
        justification: Optional[str] = None,
        overall_comment: Optional[str] = None,
        tokens_used: Optional[int] = None,
        api_call_time: Optional[float] = None,
        error_message: Optional[str] = None
    ) -> int:
        """
        Insert or update a grading result.
        
        Args:
            experiment_id: Experiment identifier (e.g., 'exp_01')
            trial_number: Trial number (1-4)
            student_id: Student identifier (e.g., 'student_00')
            student_name: Student name (e.g., 'Mahasiswa 1')
            question_number: Question number (1-7)
            question_text: The question text
            answer_text: Student's answer
            model: AI model used ('chatgpt' or 'gemini')
            strategy: Prompting strategy used
            status: Status ('pending', 'processing', 'completed', 'failed')
            grades: Dictionary of grades per criterion
            weighted_score: Calculated weighted score
            justification: AI justification
            overall_comment: AI overall comment
            tokens_used: API tokens consumed
            api_call_time: API call duration in seconds
            error_message: Error message if failed
        
        Returns:
            Row ID of inserted/updated record
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        timestamp = datetime.now().isoformat()
        grades_json = json.dumps(grades) if grades else None
        
        cursor.execute("""
            INSERT OR REPLACE INTO grading_results (
                experiment_id, trial_number, student_id, student_name,
                question_number, question_text, answer_text, model, strategy,
                grades, weighted_score, justification, overall_comment,
                tokens_used, api_call_time, timestamp, status, error_message
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            experiment_id, trial_number, student_id, student_name,
            question_number, question_text, answer_text, model, strategy,
            grades_json, weighted_score, justification, overall_comment,
            tokens_used, api_call_time, timestamp, status, error_message
        ))
        
        row_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return row_id
    
    def get_result(
        self,
        experiment_id: str,
        trial_number: int,
        student_id: str,
        question_number: int
    ) -> Optional[Dict[str, Any]]:
        """
        Get a specific grading result.
        
        Args:
            experiment_id: Experiment identifier
            trial_number: Trial number
            student_id: Student identifier
            question_number: Question number
        
        Returns:
            Dictionary with result data or None if not found
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM grading_results
            WHERE experiment_id = ?
            AND trial_number = ?
            AND student_id = ?
            AND question_number = ?
        """, (experiment_id, trial_number, student_id, question_number))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            result = dict(row)
            if result['grades']:
                result['grades'] = json.loads(result['grades'])
            return result
        return None
    
    def check_exists(
        self,
        experiment_id: str,
        trial_number: int,
        student_id: str,
        question_number: int
    ) -> bool:
        """
        Check if a grading result exists and is completed.
        
        Args:
            experiment_id: Experiment identifier
            trial_number: Trial number
            student_id: Student identifier
            question_number: Question number
        
        Returns:
            True if exists and completed, False otherwise
        """
        result = self.get_result(experiment_id, trial_number, student_id, question_number)
        return result is not None and result['status'] == 'completed'
    
    def get_pending_tasks(
        self,
        experiment_id: str,
        trial_number: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get all pending or failed tasks for an experiment.
        
        Args:
            experiment_id: Experiment identifier
            trial_number: Optional trial number filter
        
        Returns:
            List of pending task dictionaries
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if trial_number is not None:
            cursor.execute("""
                SELECT * FROM grading_results
                WHERE experiment_id = ?
                AND trial_number = ?
                AND status IN ('pending', 'processing', 'failed')
                ORDER BY student_id, question_number
            """, (experiment_id, trial_number))
        else:
            cursor.execute("""
                SELECT * FROM grading_results
                WHERE experiment_id = ?
                AND status IN ('pending', 'processing', 'failed')
                ORDER BY trial_number, student_id, question_number
            """, (experiment_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        tasks = []
        for row in rows:
            task = dict(row)
            if task['grades']:
                task['grades'] = json.loads(task['grades'])
            tasks.append(task)
        
        return tasks
    
    def get_progress(
        self,
        experiment_id: str,
        trial_number: Optional[int] = None
    ) -> Tuple[int, int, float]:
        """
        Get progress statistics for an experiment.
        
        Args:
            experiment_id: Experiment identifier
            trial_number: Optional trial number filter
        
        Returns:
            Tuple of (completed_count, total_count, percentage)
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if trial_number is not None:
            cursor.execute("""
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed
                FROM grading_results
                WHERE experiment_id = ?
                AND trial_number = ?
            """, (experiment_id, trial_number))
        else:
            cursor.execute("""
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed
                FROM grading_results
                WHERE experiment_id = ?
            """, (experiment_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        total = row['total'] or 0
        completed = row['completed'] or 0
        percentage = (completed / total * 100) if total > 0 else 0.0
        
        return completed, total, percentage
    
    def get_failed_tasks(self, experiment_id: str) -> List[Dict[str, Any]]:
        """
        Get all failed tasks with error messages.
        
        Args:
            experiment_id: Experiment identifier
        
        Returns:
            List of failed task dictionaries
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM grading_results
            WHERE experiment_id = ?
            AND status = 'failed'
            ORDER BY trial_number, student_id, question_number
        """, (experiment_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        tasks = [dict(row) for row in rows]
        return tasks
    
    def update_status(
        self,
        experiment_id: str,
        trial_number: int,
        student_id: str,
        question_number: int,
        status: str,
        error_message: Optional[str] = None
    ):
        """
        Update status of a grading task.
        
        Args:
            experiment_id: Experiment identifier
            trial_number: Trial number
            student_id: Student identifier
            question_number: Question number
            status: New status
            error_message: Optional error message
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE grading_results
            SET status = ?, error_message = ?, timestamp = ?
            WHERE experiment_id = ?
            AND trial_number = ?
            AND student_id = ?
            AND question_number = ?
        """, (status, error_message, datetime.now().isoformat(),
              experiment_id, trial_number, student_id, question_number))
        
        conn.commit()
        conn.close()
    
    def export_to_json(
        self,
        experiment_id: str,
        trial_number: int,
        output_dir: Path
    ):
        """
        Export experiment results to JSON files (one per student).
        
        Args:
            experiment_id: Experiment identifier
            trial_number: Trial number
            output_dir: Output directory path
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT DISTINCT student_id, student_name
            FROM grading_results
            WHERE experiment_id = ?
            AND trial_number = ?
            AND status = 'completed'
            ORDER BY student_id
        """, (experiment_id, trial_number))
        
        students = cursor.fetchall()
        
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for student_row in students:
            student_id = student_row['student_id']
            student_name = student_row['student_name']
            
            cursor.execute("""
                SELECT * FROM grading_results
                WHERE experiment_id = ?
                AND trial_number = ?
                AND student_id = ?
                AND status = 'completed'
                ORDER BY question_number
            """, (experiment_id, trial_number, student_id))
            
            questions = cursor.fetchall()
            
            result_data = {
                "student_id": student_id,
                "student_name": student_name,
                "experiment_id": experiment_id,
                "trial": trial_number,
                "model": questions[0]['model'] if questions else "",
                "strategy": questions[0]['strategy'] if questions else "",
                "questions": []
            }
            
            for q in questions:
                question_data = {
                    "question_id": q['question_number'],
                    "question": q['question_text'],
                    "answer": q['answer_text'],
                    "grades": json.loads(q['grades']) if q['grades'] else {},
                    "weighted_score": q['weighted_score'],
                    "justification": q['justification'],
                    "overall_comment": q['overall_comment'],
                    "metadata": {
                        "tokens_used": q['tokens_used'],
                        "api_call_time": q['api_call_time'],
                        "timestamp": q['timestamp']
                    }
                }
                result_data["questions"].append(question_data)
            
            # Save to JSON file
            filename = f"{student_id}_{student_name.replace(' ', '_')}_trial{trial_number}.json"
            output_file = output_dir / filename
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, indent=2, ensure_ascii=False)
        
        conn.close()
    
    def get_statistics(self, experiment_id: str) -> Dict[str, Any]:
        """
        Get comprehensive statistics for an experiment.
        
        Args:
            experiment_id: Experiment identifier
        
        Returns:
            Dictionary with statistics
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Overall stats
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
                SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed,
                SUM(CASE WHEN status = 'processing' THEN 1 ELSE 0 END) as processing,
                SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending,
                AVG(CASE WHEN status = 'completed' THEN tokens_used END) as avg_tokens,
                AVG(CASE WHEN status = 'completed' THEN api_call_time END) as avg_time,
                SUM(CASE WHEN status = 'completed' THEN tokens_used ELSE 0 END) as total_tokens
            FROM grading_results
            WHERE experiment_id = ?
        """, (experiment_id,))
        
        row = cursor.fetchone()
        
        stats = {
            "experiment_id": experiment_id,
            "total_tasks": row['total'] or 0,
            "completed": row['completed'] or 0,
            "failed": row['failed'] or 0,
            "processing": row['processing'] or 0,
            "pending": row['pending'] or 0,
            "progress_percentage": (row['completed'] / row['total'] * 100) if row['total'] else 0,
            "avg_tokens_per_task": round(row['avg_tokens'] or 0, 2),
            "avg_time_per_task": round(row['avg_time'] or 0, 2),
            "total_tokens_used": row['total_tokens'] or 0
        }
        
        # Per trial stats
        cursor.execute("""
            SELECT 
                trial_number,
                COUNT(*) as total,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed
            FROM grading_results
            WHERE experiment_id = ?
            GROUP BY trial_number
            ORDER BY trial_number
        """, (experiment_id,))
        
        trials = []
        for trial_row in cursor.fetchall():
            trials.append({
                "trial": trial_row['trial_number'],
                "completed": trial_row['completed'],
                "total": trial_row['total'],
                "percentage": (trial_row['completed'] / trial_row['total'] * 100) if trial_row['total'] else 0
            })
        
        stats['trials'] = trials
        
        conn.close()
        return stats
    
    def reset_failed_tasks(self, experiment_id: str) -> int:
        """
        Reset all failed tasks to pending status for retry.
        
        Args:
            experiment_id: Experiment identifier
        
        Returns:
            Number of tasks reset
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE grading_results
            SET status = 'pending', error_message = NULL
            WHERE experiment_id = ?
            AND status = 'failed'
        """, (experiment_id,))
        
        count = cursor.rowcount
        conn.commit()
        conn.close()
        
        return count
    
    def clear_experiment(self, experiment_id: str) -> int:
        """
        Delete all results for an experiment.
        
        Args:
            experiment_id: Experiment identifier
        
        Returns:
            Number of records deleted
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            DELETE FROM grading_results
            WHERE experiment_id = ?
        """, (experiment_id,))
        
        count = cursor.rowcount
        conn.commit()
        conn.close()
        
        return count
