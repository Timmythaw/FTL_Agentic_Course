# tests/test_tools.py
"""
Part C.2: Unit Tests for Tools using pytest
Tests for all three tools with success and failure cases.

Run with: uv run pytest tests/test_tools.py -v
"""

import pytest
from src.tools.execution import execute_get_time, execute_calc, execute_lookup_faq
import json


class TestGetTimeTool:
    """Unit tests for get_time tool."""
    
    def test_get_time_cape_town_success(self):
        """Test 1: Valid location - Cape Town"""
        result = execute_get_time("Cape Town")
        assert "Cape Town" in result
        assert "Error" not in result
        assert ":" in result  # Should contain time format
    
    def test_get_time_utc_success(self):
        """Test 2: Valid location - UTC"""
        result = execute_get_time("UTC")
        assert "UTC" in result
        assert "Error" not in result
    
    def test_get_time_invalid_location_failure(self):
        """Test 3 (FAILURE CASE): Invalid location should return error"""
        result = execute_get_time("Mars")
        assert "Error" in result
        assert "not supported" in result
        assert "Available locations" in result


class TestCalcTool:
    """Unit tests for calc tool."""
    
    def test_calc_percentage_success(self):
        """Test 4: Percentage calculation - 18% of 24500"""
        result = execute_calc("18% of 24500")
        assert "4410" in result or "4,410" in result
        assert "Error" not in result
        assert "Steps" in result  # Should show calculation steps
    
    def test_calc_simple_arithmetic_success(self):
        """Test 5: Simple arithmetic - 2 + 2"""
        result = execute_calc("2 + 2")
        assert "4" in result
        assert "Error" not in result
    
    def test_calc_division_by_zero_failure(self):
        """Test 6 (FAILURE CASE): Division by zero should return error"""
        result = execute_calc("100 / 0")
        assert "Error" in result
        assert "zero" in result.lower()
        assert "not allowed" in result.lower()
    
    def test_calc_invalid_characters_failure(self):
        """Test 7 (FAILURE CASE): Invalid characters should return error"""
        result = execute_calc("2 + abc")
        assert "Error" in result or "error" in result.lower()


class TestLookupFaqTool:
    """Unit tests for lookup_faq tool."""
    
    def test_faq_refund_policy_success(self):
        """Test 8: Valid FAQ query - refund policy"""
        result = execute_lookup_faq("refund policy")
        data = json.loads(result)
        assert "answer" in data
        assert "30 days" in data["answer"]
        assert "source_title" in data
    
    def test_faq_shipping_success(self):
        """Test 9: Valid FAQ query - shipping"""
        result = execute_lookup_faq("shipping")
        data = json.loads(result)
        assert "answer" in data
        assert "$50" in data["answer"] or "free" in data["answer"].lower()
    
    def test_faq_no_match_fallback_failure(self):
        """Test 10 (FAILURE CASE): Unknown topic returns fallback"""
        result = execute_lookup_faq("cryptocurrency policy")
        data = json.loads(result)
        assert "couldn't find" in data["answer"] or "No Match" in data["source_title"]
        assert "suggestion" in data or "available" in result.lower()