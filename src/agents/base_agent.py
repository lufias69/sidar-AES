"""
Base Agent Abstract Class
Defines interface for all essay grading agents
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import time
import json
from datetime import datetime


class GradingResult:
    """Structured result from essay grading"""
    
    def __init__(
        self,
        student_id: str,
        question_id: str,
        trial: int,
        model: str,
        scores: Dict[str, Dict[str, Any]],
        weighted_score: float,
        overall_comment: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.student_id = student_id
        self.question_id = question_id
        self.trial = trial
        self.model = model
        self.scores = scores  # {criterion: {grade, justification}}
        self.weighted_score = weighted_score
        self.overall_comment = overall_comment
        self.metadata = metadata or {}
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "student_id": self.student_id,
            "question_id": self.question_id,
            "trial": self.trial,
            "model": self.model,
            "scores": self.scores,
            "weighted_score": self.weighted_score,
            "overall_comment": self.overall_comment,
            "metadata": self.metadata,
            "timestamp": self.timestamp
        }
    
    def to_json(self, **kwargs) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), ensure_ascii=False, **kwargs)
    
    def __repr__(self) -> str:
        return f"GradingResult(student={self.student_id}, question={self.question_id}, score={self.weighted_score})"


class BaseAgent(ABC):
    """
    Abstract base class for essay grading agents
    All specific agents (ChatGPT, Gemini, etc.) must inherit from this
    """
    
    def __init__(
        self,
        api_key: str,
        model_name: str,
        temperature: float = 0.3,
        max_tokens: int = 2000,
        max_retries: int = 3,
        retry_delay: int = 5,
        timeout: int = 60
    ):
        self.api_key = api_key
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.timeout = timeout
        
        # Statistics
        self.total_calls = 0
        self.successful_calls = 0
        self.failed_calls = 0
        self.total_tokens = 0
    
    @abstractmethod
    def _call_api(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Make API call to the LLM
        Must be implemented by each specific agent
        
        Args:
            prompt: The grading prompt
            system_prompt: Optional system prompt
            
        Returns:
            Raw response from API
        """
        pass
    
    @abstractmethod
    def parse_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse API response into structured format
        Must be implemented by each specific agent
        
        Args:
            response: Raw API response
            
        Returns:
            Parsed grading data with scores and justifications
        """
        pass
    
    def grade_essay(
        self,
        student_id: str,
        question_id: str,
        question: str,
        answer: str,
        rubric,
        trial: int = 1,
        additional_context: Optional[str] = None,
        language: str = "indonesian"
    ) -> GradingResult:
        """
        Grade a single essay
        
        Args:
            student_id: Student identifier
            question_id: Question identifier
            question: The essay question/prompt
            answer: Student's essay answer
            rubric: Rubric object for grading
            trial: Trial number (1-4)
            additional_context: Optional additional instructions
            language: Language for justifications ("indonesian" or "english")
            
        Returns:
            GradingResult with scores and justifications
        """
        from src.core.prompt_builder import PromptBuilder
        
        # Build prompt with language and strategy support
        strategy = getattr(self, 'strategy', 'zero-shot')  # Default to zero-shot if not set
        builder = PromptBuilder(rubric, language=language, strategy=strategy)
        prompt = builder.build_grading_prompt(question, answer, additional_context)
        system_prompt = builder.get_system_prompt()
        
        # Call API with retries
        response = self._call_with_retries(prompt, system_prompt)
        
        # Parse response
        parsed = self.parse_response(response)
        
        # Calculate weighted score
        grades = {criterion: data["grade"] for criterion, data in parsed["scores"].items()}
        weighted_score = rubric.calculate_weighted_score(grades)
        
        # Create result
        result = GradingResult(
            student_id=student_id,
            question_id=question_id,
            trial=trial,
            model=self.model_name,
            scores=parsed["scores"],
            weighted_score=weighted_score,
            overall_comment=parsed.get("overall_comment"),
            metadata={
                "tokens": response.get("tokens", 0),
                "api_call_time": response.get("call_time", 0)
            }
        )
        
        self.successful_calls += 1
        return result
    
    def _call_with_retries(
        self,
        prompt: str,
        system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Call API with retry logic
        
        Args:
            prompt: The prompt
            system_prompt: Optional system prompt
            
        Returns:
            API response
            
        Raises:
            Exception: If all retries fail
        """
        self.total_calls += 1
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                start_time = time.time()
                response = self._call_api(prompt, system_prompt)
                call_time = time.time() - start_time
                
                response["call_time"] = call_time
                return response
                
            except Exception as e:
                last_error = e
                if attempt < self.max_retries - 1:
                    print(f"Attempt {attempt + 1} failed: {e}. Retrying in {self.retry_delay}s...")
                    time.sleep(self.retry_delay)
                else:
                    self.failed_calls += 1
                    print(f"All {self.max_retries} attempts failed")
        
        raise Exception(f"API call failed after {self.max_retries} attempts: {last_error}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get agent statistics"""
        return {
            "model": self.model_name,
            "total_calls": self.total_calls,
            "successful_calls": self.successful_calls,
            "failed_calls": self.failed_calls,
            "success_rate": self.successful_calls / self.total_calls if self.total_calls > 0 else 0,
            "total_tokens": self.total_tokens
        }
    
    def reset_statistics(self):
        """Reset statistics counters"""
        self.total_calls = 0
        self.successful_calls = 0
        self.failed_calls = 0
        self.total_tokens = 0
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(model={self.model_name})"


# Example validation function
def validate_grading_response(response: Dict[str, Any], expected_criteria: list) -> bool:
    """
    Validate that grading response has all required fields
    
    Args:
        response: Parsed response
        expected_criteria: List of criterion names
        
    Returns:
        True if valid, False otherwise
    """
    if "scores" not in response:
        return False
    
    scores = response["scores"]
    
    # Check all criteria present
    if set(scores.keys()) != set(expected_criteria):
        return False
    
    # Check each criterion has grade and justification
    valid_grades = {"A", "B", "C", "D/E"}
    for criterion, data in scores.items():
        if "grade" not in data or "justification" not in data:
            return False
        if data["grade"] not in valid_grades:
            return False
        if not isinstance(data["justification"], str) or len(data["justification"]) < 20:
            return False
    
    return True
