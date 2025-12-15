"""
Experiment Runner
Runs 4x trials for each model (ChatGPT and Gemini)
"""

import json
import time
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from tqdm import tqdm

from src.agents.chatgpt_agent import ChatGPTAgent
from src.agents.gemini_agent import GeminiAgent
from src.core.rubric import RubricManager
from src.utils.logger import setup_logger


class ExperimentRunner:
    """
    Runs essay grading experiments with multiple trials
    """
    
    def __init__(
        self,
        num_trials: int = 4,
        results_dir: str = "data/results",
        save_interval: int = 10,
        checkpoint_enabled: bool = True
    ):
        self.num_trials = num_trials
        self.results_dir = Path(results_dir)
        self.save_interval = save_interval
        self.checkpoint_enabled = checkpoint_enabled
        
        # Create results directories
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.chatgpt_dir = self.results_dir / "chatgpt_trials"
        self.gemini_dir = self.results_dir / "gemini_trials"
        self.chatgpt_dir.mkdir(exist_ok=True)
        self.gemini_dir.mkdir(exist_ok=True)
        
        # Logger
        self.logger = setup_logger("ExperimentRunner")
        
        # Initialize agents
        self.chatgpt_agent = None
        self.gemini_agent = None
        self.rubric = None
        
        # Results storage
        self.results = {
            "chatgpt": [],
            "gemini": []
        }
        
        # Experiment metadata
        self.metadata = {
            "start_time": None,
            "end_time": None,
            "num_trials": num_trials,
            "total_essays": 0,
            "completed_essays": 0,
            "failed_essays": 0
        }
    
    def initialize_agents(self, chatgpt_api_key: Optional[str] = None, gemini_api_key: Optional[str] = None):
        """Initialize AI agents"""
        self.logger.info("Initializing agents...")
        
        try:
            self.chatgpt_agent = ChatGPTAgent(api_key=chatgpt_api_key)
            self.logger.info(f"✓ ChatGPT agent initialized: {self.chatgpt_agent.model_name}")
        except Exception as e:
            self.logger.error(f"✗ Failed to initialize ChatGPT agent: {e}")
        
        try:
            self.gemini_agent = GeminiAgent(api_key=gemini_api_key)
            self.logger.info(f"✓ Gemini agent initialized: {self.gemini_agent.model_name}")
        except Exception as e:
            self.logger.error(f"✗ Failed to initialize Gemini agent: {e}")
    
    def load_rubric(self, rubric_id: str = "default"):
        """Load rubric"""
        manager = RubricManager()
        self.rubric = manager.get_rubric(rubric_id)
        self.logger.info(f"Loaded rubric: {self.rubric.name}")
    
    def run_single_trial(
        self,
        essays: List[Dict[str, Any]],
        model: str,
        trial: int
    ) -> List[Dict[str, Any]]:
        """
        Run a single trial
        
        Args:
            essays: List of essays to grade
            model: 'chatgpt' or 'gemini'
            trial: Trial number (1-4)
            
        Returns:
            List of grading results
        """
        agent = self.chatgpt_agent if model == "chatgpt" else self.gemini_agent
        
        if agent is None:
            self.logger.error(f"{model} agent not initialized")
            return []
        
        self.logger.info(f"Starting {model.upper()} Trial {trial}/{self.num_trials}")
        
        results = []
        failed_count = 0
        
        # Progress bar
        pbar = tqdm(essays, desc=f"{model.upper()} Trial {trial}", unit="essay")
        
        for idx, essay in enumerate(pbar):
            try:
                result = agent.grade_essay(
                    student_id=essay["student_id"],
                    question_id=essay["question_id"],
                    question=essay["question"],
                    answer=essay["answer"],
                    rubric=self.rubric,
                    trial=trial
                )
                
                results.append(result.to_dict())
                
                # Save checkpoint periodically
                if self.checkpoint_enabled and (idx + 1) % self.save_interval == 0:
                    self._save_checkpoint(model, trial, results)
                    pbar.set_postfix({"saved": idx + 1, "failed": failed_count})
                
            except Exception as e:
                self.logger.error(f"Error grading essay {essay['student_id']}-{essay['question_id']}: {e}")
                failed_count += 1
                self.metadata["failed_essays"] += 1
                pbar.set_postfix({"failed": failed_count})
        
        self.logger.info(f"Completed {model.upper()} Trial {trial}: {len(results)}/{len(essays)} essays graded")
        
        if failed_count > 0:
            self.logger.warning(f"{failed_count} essays failed during {model.upper()} Trial {trial}")
        
        return results
    
    def run_full_experiment(
        self,
        essays: List[Dict[str, Any]],
        models: List[str] = ["chatgpt", "gemini"]
    ):
        """
        Run full experiment with all trials for all models
        
        Args:
            essays: List of essays to grade
            models: List of models to use ['chatgpt', 'gemini']
        """
        self.metadata["start_time"] = datetime.now().isoformat()
        self.metadata["total_essays"] = len(essays) * len(models) * self.num_trials
        
        self.logger.info("="*80)
        self.logger.info("STARTING FULL EXPERIMENT")
        self.logger.info("="*80)
        self.logger.info(f"Essays: {len(essays)}")
        self.logger.info(f"Models: {', '.join(models)}")
        self.logger.info(f"Trials per model: {self.num_trials}")
        self.logger.info(f"Total API calls: {len(essays) * len(models) * self.num_trials}")
        self.logger.info("="*80)
        
        for model in models:
            if model == "chatgpt" and self.chatgpt_agent is None:
                self.logger.warning("Skipping ChatGPT - agent not initialized")
                continue
            if model == "gemini" and self.gemini_agent is None:
                self.logger.warning("Skipping Gemini - agent not initialized")
                continue
            
            model_results = []
            
            for trial in range(1, self.num_trials + 1):
                trial_results = self.run_single_trial(essays, model, trial)
                model_results.extend(trial_results)
                
                # Save trial results
                self._save_trial_results(model, trial, trial_results)
                
                # Brief pause between trials
                if trial < self.num_trials:
                    time.sleep(2)
            
            self.results[model] = model_results
            self.logger.info(f"✓ {model.upper()} completed: {len(model_results)} total results")
        
        self.metadata["end_time"] = datetime.now().isoformat()
        self.metadata["completed_essays"] = sum(len(results) for results in self.results.values())
        
        # Save final results
        self._save_final_results()
        
        # Print summary
        self._print_summary()
    
    def _save_checkpoint(self, model: str, trial: int, results: List[Dict[str, Any]]):
        """Save checkpoint during trial"""
        checkpoint_dir = self.chatgpt_dir if model == "chatgpt" else self.gemini_dir
        checkpoint_file = checkpoint_dir / f"trial_{trial}_checkpoint.json"
        
        with open(checkpoint_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
    
    def _save_trial_results(self, model: str, trial: int, results: List[Dict[str, Any]]):
        """Save results from a single trial"""
        trial_dir = self.chatgpt_dir if model == "chatgpt" else self.gemini_dir
        trial_file = trial_dir / f"trial_{trial}.json"
        
        with open(trial_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"Saved {model} trial {trial} results: {trial_file}")
    
    def _save_final_results(self):
        """Save final combined results"""
        # Save all results
        all_results_file = self.results_dir / "all_results.json"
        with open(all_results_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        # Save metadata
        metadata_file = self.results_dir / "experiment_metadata.json"
        
        # Add agent statistics
        if self.chatgpt_agent:
            self.metadata["chatgpt_stats"] = self.chatgpt_agent.get_statistics()
        if self.gemini_agent:
            self.metadata["gemini_stats"] = self.gemini_agent.get_statistics()
        
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"Saved final results: {all_results_file}")
        self.logger.info(f"Saved metadata: {metadata_file}")
    
    def _print_summary(self):
        """Print experiment summary"""
        self.logger.info("="*80)
        self.logger.info("EXPERIMENT COMPLETED")
        self.logger.info("="*80)
        
        # Calculate duration
        start = datetime.fromisoformat(self.metadata["start_time"])
        end = datetime.fromisoformat(self.metadata["end_time"])
        duration = (end - start).total_seconds()
        
        self.logger.info(f"Duration: {duration:.2f} seconds ({duration/60:.2f} minutes)")
        self.logger.info(f"Completed essays: {self.metadata['completed_essays']}/{self.metadata['total_essays']}")
        self.logger.info(f"Failed essays: {self.metadata['failed_essays']}")
        
        # Model statistics
        if self.chatgpt_agent:
            stats = self.chatgpt_agent.get_statistics()
            self.logger.info(f"\nChatGPT Statistics:")
            self.logger.info(f"  - Total calls: {stats['total_calls']}")
            self.logger.info(f"  - Success rate: {stats['success_rate']:.2%}")
            self.logger.info(f"  - Total tokens: {stats['total_tokens']}")
        
        if self.gemini_agent:
            stats = self.gemini_agent.get_statistics()
            self.logger.info(f"\nGemini Statistics:")
            self.logger.info(f"  - Total calls: {stats['total_calls']}")
            self.logger.info(f"  - Success rate: {stats['success_rate']:.2%}")
            self.logger.info(f"  - Estimated tokens: {stats['total_tokens']}")
        
        self.logger.info("="*80)


# Example usage
if __name__ == "__main__":
    from dotenv import load_dotenv
    from src.utils.data_loader import DataLoader
    
    load_dotenv()
    
    # Initialize runner
    runner = ExperimentRunner(num_trials=4)
    
    # Initialize agents
    runner.initialize_agents()
    
    # Load rubric
    runner.load_rubric("default")
    
    # Load data
    loader = DataLoader()
    
    # Create example data if needed
    try:
        dataset = loader.load_unified_dataset()
    except FileNotFoundError:
        print("Creating example data...")
        loader.create_example_data()
        questions = loader.load_questions("data/raw/example_questions.csv")
        answers = loader.load_student_answers("data/raw/example_student_answers.csv")
        dataset = loader.create_unified_dataset(questions, answers)
        loader.save_unified_dataset(dataset)
    
    print(f"Loaded {len(dataset)} essays")
    
    # Run on first 2 essays as demo
    demo_essays = dataset[:2]
    
    print(f"\nRunning experiment on {len(demo_essays)} essays...")
    runner.run_full_experiment(demo_essays, models=["chatgpt", "gemini"])
