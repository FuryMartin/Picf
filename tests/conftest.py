import pytest
import tempfile
import shutil
import os
from pathlib import Path
from unittest.mock import Mock, MagicMock
import numpy as np
from PIL import Image


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path)


@pytest.fixture
def sample_image():
    """Create a sample PIL Image for testing."""
    # Create a simple 100x100 RGB image
    image = Image.new('RGB', (100, 100), color='red')
    return image


@pytest.fixture
def sample_image_array():
    """Create a sample numpy array representing an image."""
    # Create a simple 100x100x3 RGB image array
    return np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)


@pytest.fixture
def temp_image_file(temp_dir, sample_image):
    """Create a temporary image file."""
    image_path = temp_dir / "test_image.jpg"
    sample_image.save(image_path)
    return image_path


@pytest.fixture
def temp_images_dir(temp_dir, sample_image):
    """Create a temporary directory with multiple test images."""
    images_dir = temp_dir / "images"
    images_dir.mkdir()
    
    # Create several test images
    for i in range(5):
        img_path = images_dir / f"image_{i}.jpg"
        # Create images with different colors
        colors = ['red', 'green', 'blue', 'yellow', 'purple']
        img = Image.new('RGB', (100, 100), color=colors[i])
        img.save(img_path)
    
    return images_dir


@pytest.fixture
def mock_config():
    """Mock configuration object."""
    config = Mock()
    config.image_dir = "/fake/path"
    config.output_dir = "/fake/output"
    config.threshold = 0.9
    config.algorithm = "phash"
    return config


@pytest.fixture
def mock_logger():
    """Mock logger for testing."""
    logger = MagicMock()
    return logger


@pytest.fixture
def sample_duplicate_mapping():
    """Sample duplicate mapping for testing."""
    return {
        'image1.jpg': ['image2.jpg', 'image3.jpg'],
        'image4.jpg': ['image5.jpg'],
        'image6.jpg': []
    }


@pytest.fixture
def sample_hash_dict():
    """Sample hash dictionary for testing."""
    return {
        'image1.jpg': 'abc123def456',
        'image2.jpg': 'def456ghi789',
        'image3.jpg': 'ghi789jkl012',
        'image4.jpg': 'jkl012mno345'
    }


@pytest.fixture
def mock_cv2_image():
    """Mock OpenCV image (BGR format)."""
    return np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)


@pytest.fixture
def temp_json_file(temp_dir):
    """Create a temporary JSON file."""
    json_path = temp_dir / "test_config.json"
    return json_path


@pytest.fixture
def sample_image_paths(temp_images_dir):
    """Get list of sample image paths."""
    return list(temp_images_dir.glob("*.jpg"))


@pytest.fixture(autouse=True)
def setup_test_environment(monkeypatch):
    """Setup test environment variables and paths."""
    # Set test-specific environment variables
    monkeypatch.setenv("PYTEST_CURRENT_TEST", "true")
    
    # Mock any external dependencies that might cause issues in testing
    import sys
    if 'tensorflow' in sys.modules:
        monkeypatch.setattr('tensorflow.config.experimental.set_memory_growth', Mock())


@pytest.fixture
def capture_logs():
    """Fixture to capture log messages during testing."""
    import logging
    import io
    
    log_capture = io.StringIO()
    handler = logging.StreamHandler(log_capture)
    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    
    yield log_capture
    
    logger.removeHandler(handler)


@pytest.fixture(scope="session")
def test_data_dir():
    """Directory for test data files."""
    test_dir = Path(__file__).parent / "test_data"
    test_dir.mkdir(exist_ok=True)
    return test_dir


# Pytest configuration hooks
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test items during collection."""
    for item in items:
        # Add unit marker to tests in unit directory
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        # Add integration marker to tests in integration directory
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)