import pytest
from rest_framework import serializers
from api.validators import RobotValidator, OrderValidator


class TestRobotValidator:
    @pytest.mark.parametrize(
        "model, version, created",
        [
            ("AB", "12", "2022-01-01"),
            ("CD", "34", "2022-02-02"),
        ],
        ids=["happy_path_1", "happy_path_2"],
    )
    def test_valid_data(self, model, version, created):
        data = {"model": model, "version": version, "created": created}
        validator = RobotValidator()
        validator(data)

    @pytest.mark.parametrize(
        "model, version, created",
        [
            ("A", "12", "2022-01-01"),
            ("AB", "1", "2022-02-02"),
            ("AB", "12", 12345),
        ],
        ids=[
            "model_length_less_than_2",
            "version_length_less_than_2",
            "invalid_created_type",
        ],
    )
    def test_invalid_data(self, model, version, created):
        data = {"model": model, "version": version, "created": created}
        validator = RobotValidator()
        with pytest.raises(serializers.ValidationError):
            validator(data)


class TestOrderValidator:
    @pytest.mark.parametrize(
        "email, robot_serial",
        [
            ("test@example.com", "A4-12"),
            ("user@example.com", "D4-4F"),
        ],
        ids=["happy_path_1", "happy_path_2"],
    )
    def test_valid_data(self, email, robot_serial):
        data = {"email": email, "robot_serial": robot_serial}
        validator = OrderValidator()
        validator(data)

    @pytest.mark.parametrize(
        "email, robot_serial",
        [
            ("test@example.com", 12345),
        ],
        ids=["invalid_robot_serial_type", "invalid_email_type"],
    )
    def test_invalid_data(self, email, robot_serial):
        data = {"email": email, "robot_serial": robot_serial}
        validator = OrderValidator()
        with pytest.raises(serializers.ValidationError):
            validator(data)

    @pytest.mark.parametrize(
        "robot_serial",
        [
            "AB12C",
            "ABC12",
            "AB12C3",
            "AB-12C",
            "AB@12C",
        ],
        ids=[
            "valid_robot_serial",
            "invalid_length_less_than_5",
            "invalid_length_greater_than_5",
            "invalid_format_hyphen",
            "invalid_format_special_character",
        ],
    )
    def test_invalid_robot_serial(self, robot_serial):
        data = {"email": "test@example.com", "robot_serial": robot_serial}
        validator = OrderValidator()
        with pytest.raises(serializers.ValidationError):
            validator(data)
