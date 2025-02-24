# import os

# def list_files(startpath, exclude=".venv"):
#     for root, dirs, files in os.walk(startpath):
#         if exclude in root:
#             continue
#         level = root.replace(startpath, "").count(os.sep)
#         indent = " " * 4 * level
#         print(f"{indent}{os.path.basename(root)}/")
#         subindent = " " * 4 * (level + 1)
#         for f in files:
#             print(f"{subindent}{f}")

# list_files(".")  # Change "." to the desired path


from sqlalchemy import create_engine, MetaData
from sqlalchemy_schemadisplay import create_schema_graph

# Replace with your actual PostgreSQL database URL
engine = create_engine("postgresql://postgres:vbvb4545@localhost:5432/college_db")

# Reflect metadata from the database
metadata = MetaData()
metadata.reflect(bind=engine)

# Generate the schema graph
graph = create_schema_graph(metadata=metadata, engine=engine)

# Save the graph as an image
graph.write_png("erd.png")

print("ER diagram saved as erd.png")


