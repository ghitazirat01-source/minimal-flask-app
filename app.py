from flask import Flask, render_template, request
from dotenv import load_dotenv
from openai import OpenAI
import os
import json

app = Flask(__name__)

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


SYSTEM_PROMPT = """
You are a contemporary art museum curator and writer.

Transform the user's description of an ordinary object into an exaggerated
contemporary-art museum wall label written in International Art English (IAE).

RULES:

1. ACCURACY
Stay faithful to the physical object described by the user.
Do not invent physical characteristics, materials, colors, damage, or
functions that were not provided. The humor comes from the contrast between
the ordinary object and inflated art-world language.

2. INTERNATIONAL ART ENGLISH
Use exaggerated IAE:
- theoretical vocabulary such as interrogate, problematize, tension,
  proposition, discursive, speculative, transversal, autonomy, materiality,
  spatiality, reality, and the Real
- abstract nouns ending in -ity, -ality, -ization, and -ion
- spatial metaphors such as space, field, site, platform, boundary,
  intersection, and framework
- long sentences with dependent clauses
- phrases such as "while simultaneously", "in relation to",
  "through which", and "insofar as"
- conceptual oppositions such as presence/absence and material/immaterial
- deliberate redundancy and lists of related concepts
- an authoritative and intellectually sophisticated curatorial tone

3. ARTISTIC SIGNIFICANCE
Treat the mundane object as if it raises important questions about
perception, materiality, identity, memory, consumption, reality,
or social structures.

4. ARTIST
Invent a fictional artist with:
- an invented name
- a short fictional biography line

Never use a real contemporary artist.

5. REQUIRED FORMAT
Return all information as JSON using the required fields.

The JSON must contain:

artist:
An invented artist name followed by a short fictional biography.

title:
An invented artwork title.

year:
The year of the artwork.

medium:
Real materials from the object combined with abstract concepts.

dimensions:
Plausible or exaggerated dimensions.

provenance:
A fictional humorous history of ownership connected to the object's
everyday life.

credit:
A fictional museum credit line.

extended_label:
An 80–120 word contemporary-art museum label.

6. PROVENANCE AND CREDIT
Create a humorous fictional history of ownership connected to the
object's everyday life.

7. EXTENDED LABEL
The extended label must contain 80–120 words.

It must mention exactly ONE invented contemporary-art theorist
and exactly ONE invented book by that theorist.

Never use real theorists or real books.

8. OVERALL TONE
The result should resemble a prestigious contemporary art museum label:
serious, intellectual, unnecessarily elaborate, and slightly absurd.

The absurdity should come from applying this language to an ordinary object.
"""


@app.route("/", methods=["GET", "POST"])
def home():
    object_description = ""
    museum_label = None

    if request.method == "POST":
        object_description = request.form["object_description"]

        response = client.responses.create(
            model="gpt-5",
            instructions=SYSTEM_PROMPT,
            input=object_description,
            text={
                "format": {
                    "type": "json_schema",
                    "name": "museum_label",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "artist": {
                                "type": "string"
                            },
                            "title": {
                                "type": "string"
                            },
                            "year": {
                                "type": "integer"
                            },
                            "medium": {
                                "type": "string"
                            },
                            "dimensions": {
                                "type": "string"
                            },
                            "provenance": {
                                "type": "string"
                            },
                            "credit": {
                                "type": "string"
                            },
                            "extended_label": {
                                "type": "string"
                            }
                        },
                        "required": [
                            "artist",
                            "title",
                            "year",
                            "medium",
                            "dimensions",
                            "provenance",
                            "credit",
                            "extended_label"
                        ],
                        "additionalProperties": False
                    },
                    "strict": True
                }
            }
        )

        museum_label = json.loads(response.output_text)

    return render_template(
        "index.html",
        object_description=object_description,
        museum_label=museum_label
    )


if __name__ == "__main__":
    app.run(debug=True, port=5001)