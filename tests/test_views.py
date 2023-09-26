import pytest
from rest_framework import status
from api.serializers import OrderSerializer
from utils.service import OrderService
from orders.views import CreateOrder
from robots.views import CreateRobotView
from api.serializers import RobotSerializer


class TestCreateOrder:
    @pytest.fixture
    def mock_serializer_class(self, mocker):
        return mocker.Mock(spec=OrderSerializer)

    @pytest.fixture
    def mock_serializer(self, mocker):
        return mocker.Mock(spec=OrderSerializer)

    @pytest.fixture
    def mock_request(self, mocker):
        return mocker.Mock()

    @pytest.fixture
    def mock_service(self, mocker):
        return mocker.Mock(spec=OrderService)

    @pytest.fixture
    def create_order_view(
        self,
        mock_serializer_class,
        mock_serializer,
        mock_request,
        mock_service,
    ):
        create_order_view = CreateOrder()
        create_order_view.serializer_class = mock_serializer_class
        mock_serializer_class.return_value = mock_serializer
        mock_serializer.is_valid.return_value = True
        mock_serializer.validated_data = {
            "email": "test@example.com",
            "robot_serial": "AB12C",
        }
        mock_request.data = {
            "email": "test@example.com",
            "robot_serial": "AB12C",
        }
        create_order_view.request = mock_request
        create_order_view.service = mock_service
        return create_order_view

    def test_post_valid_data(
        self, create_order_view, mock_serializer, mock_service
    ):
        expected_response_data = {"message": "Order processed successfully"}
        mock_service.process_order.return_value = (
            "Order processed successfully"
        )

        response = create_order_view.post(create_order_view.request)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_response_data
        mock_serializer.assert_called_once_with(
            data=create_order_view.request.data
        )
        mock_serializer.is_valid.assert_called_once()
        mock_service.assert_called_once_with("test@example.com", "AB12C")
        mock_service.process_order.assert_called_once()

    def test_post_invalid_data(
        self, create_order_view, mock_serializer, mock_service
    ):
        mock_serializer.is_valid.return_value = False
        expected_response_data = mock_serializer.errors
        expected_status_code = status.HTTP_400_BAD_REQUEST

        response = create_order_view.post(create_order_view.request)

        assert response.status_code == expected_status_code
        assert response.data == expected_response_data
        mock_serializer.assert_called_once_with(
            data=create_order_view.request.data
        )
        mock_serializer.is_valid.assert_called_once()
        mock_service.assert_not_called()


class TestCreateRobotView:
    @pytest.fixture
    def create_robot_view(self, mocker):
        create_robot_view = CreateRobotView()
        create_robot_view.queryset = mocker.Mock()
        create_robot_view.serializer_class = RobotSerializer
        return create_robot_view

    def test_get_queryset(self, create_robot_view):
        expected_queryset = create_robot_view.queryset

        queryset = create_robot_view.get_queryset()

        assert queryset == expected_queryset

    def test_get_serializer_class(self, create_robot_view):
        expected_serializer_class = RobotSerializer

        serializer_class = create_robot_view.get_serializer_class()

        assert serializer_class == expected_serializer_class

    def test_get_serializer(self, create_robot_view):
        data = {"model": "Model1", "version": "1.0", "created": "2022-01-01"}
        expected_serializer = RobotSerializer(data=data)

        serializer = create_robot_view.get_serializer(data=data)

        assert serializer == expected_serializer

    def test_perform_create(self, create_robot_view):
        serializer = RobotSerializer()
        expected_robot = serializer.save()

        robot = create_robot_view.perform_create(serializer)

        assert robot == expected_robot

    def test_post(self, create_robot_view, mocker):
        mock_request = mocker.Mock()
        mock_response = mocker.Mock()
        create_robot_view.request = mock_request
        create_robot_view.get_serializer.return_value = mocker.Mock()
        create_robot_view.perform_create.return_value = mocker.Mock()
        create_robot_view.get_serializer.return_value.data = {
            "model": "Model1",
            "version": "1.0",
            "created": "2022-01-01",
        }
        expected_response = mock_response

        response = create_robot_view.post(mock_request)

        assert response == expected_response
        create_robot_view.get_serializer.assert_called_once_with(
            data=mock_request.data
        )
        create_robot_view.get_serializer.return_value.is_valid.assert_called_once()
        create_robot_view.perform_create.assert_called_once_with(
            create_robot_view.get_serializer.return_value
        )
        create_robot_view.get_serializer.return_value.data.assert_called_once()
