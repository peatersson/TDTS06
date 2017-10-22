import javax.swing.*;
import java.util.*;

public class RouterNode {
  private int myID;
  private GuiTextArea myGUI;
  private RouterSimulator sim;
  private int[] costs = new int[RouterSimulator.NUM_NODES];
  private int[][] distance = new int[RouterSimulator.NUM_NODES][RouterSimulator.NUM_NODES];
  private int[] routes = new int[RouterSimulator.NUM_NODES];

  private boolean distance_change = false;
  private boolean poison_enabled = false;

  //--------------------------------------------------
  public RouterNode(int ID, RouterSimulator sim, int[] costs) {
    myID = ID;
    this.sim = sim;
    myGUI = new GuiTextArea("  Output window for Router #"+ ID + "  ");

    System.arraycopy(costs, 0, this.costs, 0, RouterSimulator.NUM_NODES);

    for (int i = 0; i < RouterSimulator.NUM_NODES; i++){
        if(i == myID){
            distance[i] = costs;
        } else{
            for(int j = 0; j < RouterSimulator.NUM_NODES; j++){
               distance[i][j] = RouterSimulator.INFINITY;
            }
        }
    }

    for (int i = 0; i < RouterSimulator.NUM_NODES; i++){
      if (costs[i] != RouterSimulator.INFINITY){
        routes[i] = i;
      } else {
        routes[i] = RouterSimulator.INFINITY;
      }
    }
    updateNeighbor(distance[myID]);
    printDistanceTable();
  }

  //--------------------------------------------------
  //int sourceid, int destid, int[] mincost
  public void recvUpdate(RouterPacket pkt) {
      distance[pkt.sourceid] = pkt.mincost;

      updateCosts(false);

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
      myGUI.print(distance[myID][i] + " ");
    }

    myGUI.println("\n");
  }

  //--------------------------------------------------
  public void updateLinkCost(int dest, int newcost) {
      System.out.println("1 MyID: " + myID + " Distance: " + Arrays.toString(distance[myID]));
      costs[dest] = newcost;
     /* for (int i = 0; i < RouterSimulator.NUM_NODES; i++) {
          if (routes[i] == dest){
              distance[myID][i] = newcost;
          }
      }*/
      System.out.println("2 MyID: " + myID + " Distance: " + Arrays.toString(distance[myID]));
      updateCosts(true);
    // distance_change = false;

   /* costs[dest] = newcost;


      if (costs[dest] < distance[dest]) {
      distance[dest] = costs[dest];
      routes[dest] = dest;

      distance_change = true;
    } else if (routes[dest] ==  dest){
      distance[dest] = newcost;

      distance_change = true;
    }

    if (distance_change) {
        updateNeighbor(distance[myID]);
    }*/
  }

  public void updateNeighbor(int[] distance){
      for (int i = 0; i < RouterSimulator.NUM_NODES; i++) {
          if (costs[i] != RouterSimulator.INFINITY && i != myID) {
              sendUpdate(new RouterPacket(myID, i, distance));
          }
      }
  }

  public void updateCosts(boolean link){
      distance_change = false;
      for(int dest = 0; dest < RouterSimulator.NUM_NODES; dest++){
          if(dest != myID){
              int newShortestDistance = RouterSimulator.INFINITY;
              for(int j = 0; j < RouterSimulator.NUM_NODES; j++){
                  if(costs[j] != RouterSimulator.INFINITY){
                      if(newShortestDistance > distance[j][dest] + costs[j]){  //distance[myID][dest] > distance[j][dest] + costs[j]){
                          //if(link)
                            //  System.out.println("ID: " + myID+ " j: " + j + " dest: " + dest + " myID distance: " + distance[myID][dest] + " costs: " + costs[j] + " distance J: " + distance[j][dest]+ " route: " + routes[dest]);
                          distance[myID][dest] = distance[j][dest] + costs[j];
                          newShortestDistance = distance[myID][dest];
                          routes[dest] = j;
                          distance_change = true;
                      }
                  }
              }
          }
      }

      if (distance_change) {
          System.out.println("ID: " + myID+ " myID distance: " + Arrays.toString(distance[myID]) + " costs: " + Arrays.toString(costs) + " distance J: " + " route: " + Arrays.toString(routes));
          updateNeighbor(distance[myID]);
      }
  }
}


