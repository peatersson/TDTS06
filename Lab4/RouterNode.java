import javax.swing.*;

public class RouterNode {
  private int myID;
  private GuiTextArea myGUI;
  private RouterSimulator sim;
  private int[] costs = new int[RouterSimulator.NUM_NODES];
  private int[] distance = new int[RouterSimulator.NUM_NODES];
  private Integer[] routes = new Integer[RouterSimulator.NUM_NODES];

  private boolean distance_change = false;
  private boolean poison_enabled = false;

  //--------------------------------------------------
  public RouterNode(int ID, RouterSimulator sim, int[] costs) {
    myID = ID;
    this.sim = sim;
    myGUI = new GuiTextArea("  Output window for Router #"+ ID + "  ");

    System.arraycopy(costs, 0, this.costs, 0, RouterSimulator.NUM_NODES);

    for (int i = 0; i < this.sim.NUM_NODES; i++){
      distance[i] = costs[i];
    }

    for (int i = 0; i < this.sim.NUM_NODES; i++){
      if (costs[i] != this.sim.INFINITY){
        routes[i] = i;
        sendUpdate(new RouterPacket(myID, i, distance));
      } else {
        routes[i] = null;
      }
    }

    printDistanceTable();
  }

  //--------------------------------------------------
  public void recvUpdate(RouterPacket pkt) {
    distance_change = false;

    for (int i = 0; i < this.sim.NUM_NODES; i++){
      if (distance[i] > pkt.mincost[i] + distance[pkt.sourceid]){
        distance[i] = pkt.mincost[i] + distance[pkt.sourceid];
        routes[i] = routes[pkt.sourceid];

        distance_change = true;
      }
    }

    if (distance_change) {
      for (int i = 0; i < this.sim.NUM_NODES; i++) {
        if (costs[i] != this.sim.INFINITY) {
          sendUpdate(new RouterPacket(myID, i, distance));
        }
      }
    }
  }

  //--------------------------------------------------
  private void sendUpdate(RouterPacket pkt) {
    sim.toLayer2(pkt);
  }
  

  //--------------------------------------------------
  public void printDistanceTable() {
    myGUI.println("Current table for " + myID +
			"  at time " + sim.getClocktime());

    myGUI.print("I: ");
    for(int i = 0; i < routes.length; i++){
      myGUI.print(i + " ");
    }
    myGUI.println();

    myGUI.print("R: ");
    for(int i = 0; i < routes.length; i++){
      myGUI.print(routes[i] + " ");
    }

    myGUI.println();
    myGUI.print("C: ");
    for(int i = 0; i < costs.length; i++){
      myGUI.print(costs[i] + " ");
    }

    myGUI.println();
    myGUI.print("D: ");
    for(int i = 0; i < distance.length; i++){
      myGUI.print(distance[i] + " ");
    }

    myGUI.println("\n");
  }

  //--------------------------------------------------
  public void updateLinkCost(int dest, int newcost) {
    distance_change = false;

    costs[dest] = newcost;

    if (costs[dest] < distance[dest]) {
      distance[dest] = costs[dest];
      routes[dest] = dest;
    }

    for (int i = 0; i < this.sim.NUM_NODES; i++) {
      if (costs[i] != this.sim.INFINITY) {
        sendUpdate(new RouterPacket(myID, i, distance));
      }
    }
  }
}


