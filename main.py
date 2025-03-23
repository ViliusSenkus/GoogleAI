import base64
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

gemini_api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(
        api_key=gemini_api_key,
    )
model = "gemini-2.0-flash"

### TEXT-2-TEXT EXAMPLE ###

def text_request():

  response = client.models.generate_content(
      model=model,
      contents=[
          types.Part.from_text(text="""Who are you?"""),
      ]
  )
  print(response.text)

    # contents = [
    #     types.Content(
    #         role="user",
    #         parts=[
    #             types.Part.from_text(text="""Who are you?"""),
    #         ],
    #     ),
    # ]
    # generate_content_config = types.GenerateContentConfig(
    #     temperature=1,
    #     top_p=0.95,
    #     top_k=40,
    #     max_output_tokens=8192,
    #     response_mime_type="text/plain",
    # )

    # for chunk in client.models.generate_content_stream(
    #     model=model,
    #     contents=contents,
    #     config=generate_content_config,
    # ):
        # print(chunk.text, end="")


### IMAGE-2-TEXT EXAMPLE ###

def picture_request():
  with open("image.WEBP", "rb") as f:
      image = f.read()

  response = client.models.generate_content(
      model=model,
      contents=[
          types.Part.from_bytes(data=image, mime_type="image/png"),
          "Write a short and engaging blog post based on this picture.",
      ]
  )
  print(response.text)


if __name__ == "__main__":
    text_request()
    picture_request()
