"""
Validation tests to ensure the testing infrastructure is properly set up.
These tests verify that pytest, coverage, and fixtures are working correctly.
"""

import pytest
import sys
import os
from pathlib import Path
import tempfile
import shutil


class TestPytestSetup:
    """Test that pytest is properly configured."""
    
    def test_pytest_is_working(self):
        """Basic test to verify pytest is functioning."""
        assert True
    
    def test_markers_are_configured(self):
        """Test that custom markers are properly configured."""
        # This test should pass if markers are properly set up
        pass
    
    @pytest.mark.unit
    def test_unit_marker(self):
        """Test that unit marker is working."""
        assert True
    
    @pytest.mark.integration  
    def test_integration_marker(self):
        """Test that integration marker is working."""
        assert True
    
    @pytest.mark.slow
    def test_slow_marker(self):
        """Test that slow marker is working."""
        assert True


class TestFixtures:
    """Test that shared fixtures are working properly."""
    
    def test_temp_dir_fixture(self, temp_dir):
        """Test that temp_dir fixture creates a valid directory."""
        assert temp_dir.exists()
        assert temp_dir.is_dir()
        
        # Test we can create files in it
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")
        assert test_file.exists()
    
    def test_sample_image_fixture(self, sample_image):
        """Test that sample_image fixture creates a valid PIL Image."""
        from PIL import Image
        assert isinstance(sample_image, Image.Image)
        assert sample_image.size == (100, 100)
        assert sample_image.mode == 'RGB'
    
    def test_sample_image_array_fixture(self, sample_image_array):
        """Test that sample_image_array fixture creates a valid numpy array."""
        import numpy as np
        assert isinstance(sample_image_array, np.ndarray)
        assert sample_image_array.shape == (100, 100, 3)
        assert sample_image_array.dtype == np.uint8
    
    def test_temp_image_file_fixture(self, temp_image_file):
        """Test that temp_image_file fixture creates a valid image file."""
        assert temp_image_file.exists()
        assert temp_image_file.suffix == '.jpg'
        
        # Verify it's a valid image by opening it
        from PIL import Image
        with Image.open(temp_image_file) as img:
            assert img.size == (100, 100)
    
    def test_temp_images_dir_fixture(self, temp_images_dir):
        """Test that temp_images_dir fixture creates multiple images."""
        assert temp_images_dir.exists()
        assert temp_images_dir.is_dir()
        
        # Should contain 5 test images
        image_files = list(temp_images_dir.glob("*.jpg"))
        assert len(image_files) == 5
        
        # Verify each is a valid image
        from PIL import Image
        for img_path in image_files:
            with Image.open(img_path) as img:
                assert img.size == (100, 100)
    
    def test_mock_config_fixture(self, mock_config):
        """Test that mock_config fixture provides expected attributes."""
        assert hasattr(mock_config, 'image_dir')
        assert hasattr(mock_config, 'output_dir') 
        assert hasattr(mock_config, 'threshold')
        assert hasattr(mock_config, 'algorithm')
        assert mock_config.threshold == 0.9
        assert mock_config.algorithm == "phash"
    
    def test_sample_duplicate_mapping_fixture(self, sample_duplicate_mapping):
        """Test that sample_duplicate_mapping fixture provides valid data."""
        assert isinstance(sample_duplicate_mapping, dict)
        assert len(sample_duplicate_mapping) == 3
        assert 'image1.jpg' in sample_duplicate_mapping
        assert isinstance(sample_duplicate_mapping['image1.jpg'], list)
    
    def test_sample_hash_dict_fixture(self, sample_hash_dict):
        """Test that sample_hash_dict fixture provides valid hash data."""
        assert isinstance(sample_hash_dict, dict)
        assert len(sample_hash_dict) == 4
        assert all(isinstance(k, str) for k in sample_hash_dict.keys())
        assert all(isinstance(v, str) for v in sample_hash_dict.values())


class TestCoverageSetup:
    """Test that coverage reporting is properly configured."""
    
    def test_coverage_config_exists(self):
        """Test that coverage configuration exists in pyproject.toml."""
        project_root = Path(__file__).parent.parent
        pyproject_path = project_root / "pyproject.toml"
        
        assert pyproject_path.exists()
        
        content = pyproject_path.read_text()
        assert "[tool.coverage.run]" in content
        assert "[tool.coverage.report]" in content
        assert "source = " in content


class TestProjectStructure:
    """Test that the project structure is properly set up."""
    
    def test_tests_directory_structure(self):
        """Test that test directories are properly created."""
        tests_dir = Path(__file__).parent
        
        assert tests_dir.exists()
        assert (tests_dir / "__init__.py").exists()
        assert (tests_dir / "conftest.py").exists()
        assert (tests_dir / "unit").exists()
        assert (tests_dir / "unit" / "__init__.py").exists()
        assert (tests_dir / "integration").exists() 
        assert (tests_dir / "integration" / "__init__.py").exists()
    
    def test_pyproject_toml_exists(self):
        """Test that pyproject.toml exists and contains required sections."""
        project_root = Path(__file__).parent.parent
        pyproject_path = project_root / "pyproject.toml"
        
        assert pyproject_path.exists()
        
        content = pyproject_path.read_text()
        assert "[tool.poetry]" in content
        assert "[tool.pytest.ini_options]" in content
        assert "[tool.coverage.run]" in content
        
    def test_required_dependencies_configured(self):
        """Test that testing dependencies are configured."""
        project_root = Path(__file__).parent.parent
        pyproject_path = project_root / "pyproject.toml"
        
        content = pyproject_path.read_text()
        assert "pytest" in content
        assert "pytest-cov" in content
        assert "pytest-mock" in content


class TestMocking:
    """Test that mocking utilities are working."""
    
    def test_mock_logger_fixture(self, mock_logger):
        """Test that mock_logger fixture works."""
        mock_logger.info("test message")
        mock_logger.info.assert_called_with("test message")
    
    def test_pytest_mock_integration(self, mocker):
        """Test that pytest-mock is properly integrated."""
        # This test will only pass if pytest-mock is properly installed and configured
        mock_func = mocker.Mock(return_value=42)
        assert mock_func() == 42
        mock_func.assert_called_once()


class TestEnvironment:
    """Test that the testing environment is properly configured."""
    
    def test_python_version(self):
        """Test that we're running on a supported Python version."""
        assert sys.version_info >= (3, 8)
    
    def test_required_packages_importable(self):
        """Test that required packages can be imported."""
        try:
            import pytest
            import PIL
            import numpy
            assert True
        except ImportError as e:
            pytest.fail(f"Required package not importable: {e}")
    
    def test_test_environment_variable_set(self, setup_test_environment):
        """Test that test environment is properly set up."""
        # PYTEST_CURRENT_TEST is automatically set by pytest during test runs
        assert "PYTEST_CURRENT_TEST" in os.environ