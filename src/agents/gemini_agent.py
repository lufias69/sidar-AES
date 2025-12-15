"""
Gemini Agent Implementation
Uses Google Gemini API for essay grading
"""

import json
import os
from typing import Dict, Any, Optional
import google.generativeai as genai
from src.agents.base_agent import BaseAgent


class GeminiAgent(BaseAgent):
    """Gemini-based essay grading agent"""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: str = "gemini-2.5-flash",
        temperature: float = 0.3,
        max_tokens: int = 4000,
        max_retries: int = 3,
        retry_delay: int = 10,  # Increased to 10s to handle rate limits (10 req/min = 6s minimum)
        timeout: int = 60,
        rubric = None,
        language: str = "indonesian",
        strategy: str = "zero-shot"
    ):
        # Get API key from environment if not provided
        if api_key is None:
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("Google API key must be provided or set in GOOGLE_API_KEY environment variable")
        
        super().__init__(
            api_key=api_key,
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            max_retries=max_retries,
            retry_delay=retry_delay,
            timeout=timeout
        )
        
        # Store rubric, language, and strategy
        self.rubric = rubric
        self.language = language
        self.strategy = strategy
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        
        # Initialize model
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config={
                "temperature": self.temperature,
                "max_output_tokens": self.max_tokens,
                "top_p": 1.0,
                "top_k": 40,
            }
        )
    
    def _call_api(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Call Gemini API
        
        Args:
            prompt: The grading prompt
            system_prompt: System prompt (prepended to user prompt for Gemini)
            
        Returns:
            Response with content and metadata
        """
        import time
        
        # Combine system prompt with user prompt (Gemini doesn't have separate system role)
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n---\n\n{prompt}"
        
        # Add explicit JSON instruction
        full_prompt += "\n\nIMPORTANT: Respond with ONLY valid JSON. No other text before or after the JSON."
        
        # Make API call
        response = self.model.generate_content(full_prompt)
        
        # Extract text
        content = response.text
        
        # Gemini doesn't provide token counts in the same way, estimate if needed
        # For now, use approximate count (rough estimate: 1 token ≈ 4 characters)
        estimated_tokens = len(full_prompt + content) // 4
        self.total_tokens += estimated_tokens
        
        # IMPORTANT: Add delay to respect rate limits (10 requests/min = 6s minimum)
        time.sleep(7)  # 7 seconds ensures we stay under 10 req/min
        
        return {
            "content": content,
            "tokens": estimated_tokens,
            "model": self.model_name,
            "finish_reason": "stop"  # Gemini uses different finish reasons
        }
    
    def parse_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse Gemini response
        
        Args:
            response: Raw API response
            
        Returns:
            Parsed grading data
            
        Raises:
            ValueError: If response format is invalid
        """
        content = response["content"].strip()
        
        # Sometimes Gemini adds markdown code blocks, remove them
        if content.startswith("```json"):
            content = content[7:]  # Remove ```json
        if content.startswith("```"):
            content = content[3:]  # Remove ```
        if content.endswith("```"):
            content = content[:-3]  # Remove trailing ```
        content = content.strip()
        
        try:
            # Parse JSON
            parsed = json.loads(content)
            
            # Validate structure
            if "scores" not in parsed:
                raise ValueError("Response missing 'scores' field")
            
            # Ensure all scores have grade and justification
            for criterion, data in parsed["scores"].items():
                if "grade" not in data:
                    raise ValueError(f"Criterion '{criterion}' missing 'grade'")
                if "justification" not in data:
                    raise ValueError(f"Criterion '{criterion}' missing 'justification'")
                
                # Validate grade
                if data["grade"] not in ["A", "B", "C", "D/E"]:
                    raise ValueError(f"Invalid grade '{data['grade']}' for criterion '{criterion}'")
            
            return parsed
        except json.JSONDecodeError as e:
            # Better error message for truncated responses
            raise ValueError(f"Failed to parse JSON response (possibly truncated): {str(e)}\nContent preview: {content[:200]}...")
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON response: {e}\nContent: {content}")
        except Exception as e:
            raise ValueError(f"Invalid response format: {e}\nContent: {content}")
    
    def grade_batch(
        self,
        essays: list,
        rubric,
        trial: int = 1,
        show_progress: bool = True
    ) -> list:
        """
        Grade multiple essays
        
        Args:
            essays: List of dicts with student_id, question_id, question, answer
            rubric: Rubric object
            trial: Trial number
            show_progress: Show progress bar
            
        Returns:
            List of GradingResult objects
        """
        results = []
        
        if show_progress:
            try:
                from tqdm import tqdm
                iterator = tqdm(essays, desc=f"Gemini Trial {trial}")
            except ImportError:
                iterator = essays
                print(f"Grading {len(essays)} essays with Gemini (trial {trial})...")
        else:
            iterator = essays
        
        for essay in iterator:
            try:
                result = self.grade_essay(
                    student_id=essay["student_id"],
                    question_id=essay["question_id"],
                    question=essay["question"],
                    answer=essay["answer"],
                    rubric=rubric,
                    trial=trial
                )
                results.append(result)
            except Exception as e:
                print(f"Error grading essay {essay.get('student_id')}: {e}")
                # Continue with next essay
        
        return results


# Example usage and testing
if __name__ == "__main__":
    from dotenv import load_dotenv
    from src.core.rubric import RubricManager
    
    # Load environment variables
    load_dotenv()
    
    # Check if API key is available
    if not os.getenv("GOOGLE_API_KEY"):
        print("Warning: GOOGLE_API_KEY not found in environment")
        print("Set it in .env file to test the agent")
    else:
        # Initialize agent
        agent = GeminiAgent()
        print(f"Initialized {agent}")
        
        # Load rubric
        manager = RubricManager()
        rubric = manager.get_rubric("default")
        
        # Test essay
        test_question = "Jelaskan konsep Automated Essay Scoring (AES) dan implikasinya untuk pendidikan."
        test_answer = """
        Automated Essay Scoring (AES) adalah sistem yang menggunakan kecerdasan buatan
        untuk menilai esai secara otomatis. Sistem ini bekerja dengan menganalisis berbagai
        aspek dari sebuah esai seperti konten, struktur, tata bahasa, dan koherensi.
        
        AES memiliki beberapa implikasi penting untuk pendidikan. Pertama, sistem ini dapat
        mengurangi beban kerja guru dalam menilai esai, terutama untuk kelas besar. Kedua,
        AES dapat memberikan feedback yang cepat kepada siswa, memungkinkan mereka untuk
        belajar dari kesalahan dengan lebih efisien.
        
        Namun, ada juga beberapa tantangan. Sistem AES mungkin kesulitan dalam menilai
        aspek kreatif dan pemikiran kritis. Selain itu, ada kekhawatiran tentang bias
        dalam algoritma yang dapat mempengaruhi keadilan penilaian.
        """
        
        print("\nTesting essay grading...")
        try:
            result = agent.grade_essay(
                student_id="TEST001",
                question_id="Q1",
                question=test_question,
                answer=test_answer,
                rubric=rubric,
                trial=1
            )
            
            print("\n" + "="*80)
            print("GRADING RESULT:")
            print("="*80)
            print(f"Student: {result.student_id}")
            print(f"Weighted Score: {result.weighted_score}/4.0")
            print("\nScores by Criterion:")
            for criterion, data in result.scores.items():
                print(f"\n{criterion}: {data['grade']} ({rubric.scale[data['grade']]} points)")
                print(f"Justification: {data['justification']}")
            
            if result.overall_comment:
                print(f"\nOverall: {result.overall_comment}")
            
            print(f"\nTokens used (estimated): {result.metadata.get('tokens', 'N/A')}")
            print(f"API call time: {result.metadata.get('api_call_time', 'N/A'):.2f}s")
            
            print("\n" + "="*80)
            print("Agent Statistics:")
            print("="*80)
            stats = agent.get_statistics()
            for key, value in stats.items():
                print(f"{key}: {value}")
                
        except Exception as e:
            print(f"Error during grading: {e}")
