from sqlalchemy_data_model_visualizer import add_web_font_and_interactivity
from sqlalchemy_data_model_visualizer import generate_data_model_diagram

from src.db.models import ChannelErrorOrm
from src.db.models import ChannelOrm
from src.db.models import MessageLogOrm
from src.db.models import UserOrm


def generate():
    models = [UserOrm, MessageLogOrm, ChannelOrm, ChannelErrorOrm]
    generate_data_model_diagram(models=models, output_file="db-schema", add_labels=True)
    add_web_font_and_interactivity(
        input_svg_file="db-schema.svg", output_svg_file="db-schema"
    )


generate()
