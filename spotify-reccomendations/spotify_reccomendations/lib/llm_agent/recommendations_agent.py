from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import Annotated, TypedDict
from langchain.chat_models import init_chat_model
from IPython.display import display, Image

from spotify_reccomendations.lib.models.user_details import SpotifyUser
from spotify_reccomendations.lib.models.top_tracks import TopTracks


class State(TypedDict):
    messages: Annotated[list, add_messages]
    user_details: SpotifyUser
    top_tracks: TopTracks


class RecommendationsAgent:
    def __init__(self, user_details: SpotifyUser, top_tracks: TopTracks):
        self.graph = StateGraph(State)
        self.user_details = user_details
        self.top_tracks = top_tracks
        self.llm = init_chat_model(model="openai:gpt-4.1")

    def chatbot(self, state: State) -> State:
        return {"messages": self.llm.invoke(state["messages"])}

    def graph_builder(self):
        self.graph.add_node("chatbot", self.chatbot)
        self.graph.add_edge(START, "chatbot")
        self.graph.add_edge("chatbot", END)

    def run(self):
        self.graph_builder()
        compiled_graph = self.graph.compile()
        self.display_graph(compiled_graph)
        return compiled_graph

    def display_graph(self, compiled_graph):
        display(Image(compiled_graph.get_graph().draw_mermaid_png()))

    def generate_music_profile(self, compiled_graph):

        track_list = "\n".join(
            f"{i+1}. {track.get('name')} by {track.get('artist')}"
            for i, track in enumerate(self.top_tracks.dataframe.to_dicts())
        )

        for event in compiled_graph.stream(
            {
                "messages": [
                    (
                        "user",
                        f"Here are my top tracks:\n{track_list}, pretend to be a music expert and provide me a fun personality based music profile that summarizes my music taste. Avoid including introductions or anything else that is not the profile.",
                    )
                ],
                "user_details": self.user_details,
                "top_tracks": self.top_tracks,
            }
        ):

            for value in event.values():
                if isinstance(value, dict) and "messages" in value:
                    return value["messages"].content

    def generate_music_recommendations(self, compiled_graph):

        track_list = "\n".join(
            f"{i+1}. {track.get('name')} by {track.get('artist')}"
            for i, track in enumerate(self.top_tracks.dataframe.to_dicts())
        )

        for event in compiled_graph.stream(
            {
                "messages": [
                    (
                        "user",
                        f"Here are my top tracks:\n{track_list}, generate 10 recommendations for me based on my music taste. \n\nreturn them in a json format with the following keys: name, artist, spotify_id.\n\nDon't include any other text or formatting I want to pass the string to json.loads() Make sure that spotify_id is the valid Spotify track ID that can be directly used in the Spotify API to get track details.",
                    )
                ],
                "user_details": self.user_details,
                "top_tracks": self.top_tracks,
            }
        ):

            for value in event.values():
                if isinstance(value, dict) and "messages" in value:
                    return value["messages"].content
