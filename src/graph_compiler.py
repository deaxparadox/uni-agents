from ai import graphs
from ai.graphs.enterpreneur_graph import entrepreneur_graph_builder

async def complie_graphs():
    graphs.entrepreneur_graph = await entrepreneur_graph_builder()