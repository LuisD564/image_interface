from unittest.mock import MagicMock, PropertyMock, call, patch
import pytest
import numpy as np

from get_images import GetImages


@pytest.fixture(scope='function')
def get_images_fixture():
    with patch.object(GetImages, 'train_model'):
        get_images = GetImages(number_of_epochs=30, batch_size=30, validation_split=0.2)
        get_images.train_model = MagicMock()
        return get_images

@patch('get_images.np')
def test_generate_circle_image_no_circles(mock_np, get_images_fixture):
    get_images_fixture.generate_circle_image((64, 64), with_circle=False)
    mock_np.zeros.assert_called()

@patch('get_images.cv2')
@patch('get_images.np')
def test_generate_circle_image(mock_np, mock_cv2, get_images_fixture):
    get_images_fixture.generate_circle_image((64, 64), with_circle=True)
    mock_np.random.randint.assert_called()
    mock_cv2.circle.assert_called()

@patch('get_images.cv2')
@patch('get_images.np')
def test_predict_circle_not_circle(mock_np, mock_cv2, get_images_fixture):
    image = np.zeros(get_images_fixture.image_size + (1,), dtype=np.uint8)
    get_images_fixture.model = MagicMock()
    get_images_fixture.model.predict.return_value = [[0.3]]
    expected_result = False
    result = get_images_fixture.predict_circle(image, get_images_fixture.image_size)

    assert expected_result == result

@patch('get_images.cv2')
@patch('get_images.np')
def test_predict_circle_not_circle(mock_np, mock_cv2, get_images_fixture):
    image = np.zeros(get_images_fixture.image_size + (1,), dtype=np.uint8)
    get_images_fixture.model = MagicMock()
    get_images_fixture.model.predict.return_value = [[0.6]]
    expected_result = True
    result = get_images_fixture.predict_circle(image, get_images_fixture.image_size)

    assert expected_result == result


