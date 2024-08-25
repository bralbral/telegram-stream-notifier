from sqlalchemy_data_model_visualizer import add_web_font_and_interactivity
from sqlalchemy_data_model_visualizer import generate_data_model_diagram

from src.db.models import ChannelORM
from src.db.models import ChannelTypeORM
from src.db.models import MessageLogORM
from src.db.models import UserORM


def generate():
    models = [UserORM, MessageLogORM, ChannelORM, ChannelTypeORM]
    generate_data_model_diagram(models=models, output_file="db-schema", add_labels=True)
    add_web_font_and_interactivity(
        input_svg_file="db-schema.svg", output_svg_file="db-schema"
    )


generate()
