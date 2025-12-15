"""
Core Rubric Management System
Handles rubric loading, validation, and weighting
"""

import json
from typing import Dict, List, Optional
from pathlib import Path
from pydantic import BaseModel, Field, validator


class GradeDescriptor(BaseModel):
    """Grade descriptor with justification indicators"""
    description: str
    points: int
    indicators: List[str] = Field(default_factory=list)
    
    @validator('points')
    def validate_points(cls, v):
        if not 1 <= v <= 4:
            raise ValueError('Points must be between 1 and 4')
        return v


class Criterion(BaseModel):
    """Single evaluation criterion"""
    weight: float
    description: str
    grades: Dict[str, GradeDescriptor]
    
    @validator('weight')
    def validate_weight(cls, v):
        if not 0 < v <= 1:
            raise ValueError('Weight must be between 0 and 1')
        return v
    
    @validator('grades')
    def validate_grades(cls, v):
        required_grades = {'A', 'B', 'C', 'D/E'}
        if set(v.keys()) != required_grades:
            raise ValueError(f'Grades must include exactly: {required_grades}')
        return v


class RubricMetadata(BaseModel):
    """Rubric metadata"""
    version: str = "1.0"
    created: str = ""
    author: str = ""
    notes: str = ""


class Rubric(BaseModel):
    """Complete rubric with multiple criteria"""
    name: str
    description: str
    criteria: Dict[str, Criterion]
    scale: Dict[str, int]
    metadata: Optional[RubricMetadata] = None
    
    @validator('criteria')
    def validate_weights_sum(cls, v):
        total_weight = sum(criterion.weight for criterion in v.values())
        if not 0.99 <= total_weight <= 1.01:  # Allow small floating point errors
            raise ValueError(f'Criterion weights must sum to 1.0, got {total_weight}')
        return v
    
    @validator('scale')
    def validate_scale(cls, v):
        required_grades = {'A', 'B', 'C', 'D/E'}
        if set(v.keys()) != required_grades:
            raise ValueError(f'Scale must include exactly: {required_grades}')
        return v
    
    def get_criterion(self, name: str) -> Criterion:
        """Get criterion by name"""
        if name not in self.criteria:
            raise ValueError(f"Criterion '{name}' not found in rubric")
        return self.criteria[name]
    
    def get_max_score(self) -> float:
        """Calculate maximum possible weighted score"""
        return sum(criterion.weight * 4 for criterion in self.criteria.values())
    
    def calculate_weighted_score(self, grades: Dict[str, str]) -> float:
        """
        Calculate weighted score from grades
        
        Args:
            grades: Dict mapping criterion name to grade (A, B, C, D/E)
            
        Returns:
            Weighted score (0.0 to 4.0)
        """
        total_score = 0.0
        for criterion_name, grade in grades.items():
            criterion = self.get_criterion(criterion_name)
            points = self.scale[grade]
            total_score += criterion.weight * points
        return round(total_score, 2)
    
    def get_grade_description(self, criterion_name: str, grade: str) -> str:
        """Get description for a specific grade in a criterion"""
        criterion = self.get_criterion(criterion_name)
        return criterion.grades[grade].description
    
    def get_grade_indicators(self, criterion_name: str, grade: str) -> List[str]:
        """Get indicators for a specific grade in a criterion"""
        criterion = self.get_criterion(criterion_name)
        return criterion.grades[grade].indicators
    
    def to_prompt_text(self) -> str:
        """
        Convert rubric to formatted text for AI prompts
        
        Returns:
            Formatted string representation of the rubric
        """
        lines = [
            f"# {self.name}",
            f"{self.description}",
            "",
            "## Evaluation Criteria:",
            ""
        ]
        
        for criterion_name, criterion in self.criteria.items():
            lines.append(f"### {criterion_name} (Weight: {criterion.weight:.0%})")
            lines.append(f"*{criterion.description}*")
            lines.append("")
            
            for grade, descriptor in criterion.grades.items():
                lines.append(f"**Grade {grade} ({descriptor.points} points):** {descriptor.description}")
                if descriptor.indicators:
                    lines.append("  - " + "\n  - ".join(descriptor.indicators))
                lines.append("")
        
        return "\n".join(lines)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return self.dict()
    
    @classmethod
    def from_dict(cls, data: Dict) -> "Rubric":
        """Create rubric from dictionary"""
        return cls(**data)


class RubricManager:
    """Manages loading and accessing rubrics"""
    
    def __init__(self, rubric_file: str = "config/rubrics.json"):
        self.rubric_file = Path(rubric_file)
        self.rubrics: Dict[str, Rubric] = {}
        self._load_rubrics()
    
    def _load_rubrics(self):
        """Load all rubrics from file"""
        if not self.rubric_file.exists():
            raise FileNotFoundError(f"Rubric file not found: {self.rubric_file}")
        
        with open(self.rubric_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for rubric_id, rubric_data in data.items():
            try:
                self.rubrics[rubric_id] = Rubric.from_dict(rubric_data)
            except Exception as e:
                print(f"Warning: Failed to load rubric '{rubric_id}': {e}")
    
    def get_rubric(self, rubric_id: str = "default") -> Rubric:
        """Get rubric by ID"""
        if rubric_id not in self.rubrics:
            raise ValueError(f"Rubric '{rubric_id}' not found. Available: {list(self.rubrics.keys())}")
        return self.rubrics[rubric_id]
    
    def list_rubrics(self) -> List[str]:
        """List all available rubric IDs"""
        return list(self.rubrics.keys())
    
    def add_rubric(self, rubric_id: str, rubric: Rubric):
        """Add a new rubric"""
        self.rubrics[rubric_id] = rubric
    
    def save_rubrics(self):
        """Save all rubrics to file"""
        data = {rubric_id: rubric.to_dict() for rubric_id, rubric in self.rubrics.items()}
        with open(self.rubric_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


# Example usage and testing
if __name__ == "__main__":
    # Test loading default rubric
    manager = RubricManager()
    rubric = manager.get_rubric("default")
    
    print("Loaded rubric:", rubric.name)
    print("\nCriteria:", list(rubric.criteria.keys()))
    print("\nMax score:", rubric.get_max_score())
    
    # Test scoring
    test_grades = {
        "Pemahaman Konten": "A",
        "Organisasi & Struktur": "B",
        "Argumen & Bukti": "B",
        "Gaya Bahasa & Mekanik": "A"
    }
    score = rubric.calculate_weighted_score(test_grades)
    print(f"\nTest grades: {test_grades}")
    print(f"Weighted score: {score}")
    
    # Test prompt generation
    print("\n" + "="*50)
    print("Rubric as prompt text:")
    print("="*50)
    print(rubric.to_prompt_text())
