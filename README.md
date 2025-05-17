# Network_graduate-
It is the final project of Advanced Network during my master studies


Project Objective

The goal of this project is to analyze the impact of flow scheduling algorithms on the performance of a data center network.
Assumptions and Inputs

    Topology: Fat-tree with 4-port switches (16 servers).

    Destination Distribution: Uniform (each flow’s destination is randomly selected).

    Number of Flows per Server: A random integer in the range [5, 15].

    Probability of a Flow Being Mice: A random value in the range [70%, 95%].

    Length of a Mice Flow: A random integer in the range [2, 20] packets.

    Length of an Elephant Flow: A random integer in the range [500, 1000] packets.

    Output Link Buffer Size: 32 packets.

    Link Transmission: Each link can transmit one packet per time slot.

Scheduling Algorithms

Per-Packet Scheduling:

    Random: Randomly selects one suitable output link among available options.

Per-Flow Scheduling:
2. ECMP (Equal-Cost Multi-Path): Randomly selects one suitable output link among available paths.

Note: Both algorithms must be implemented and compared.
Performance Metrics

    Average Flow Completion Time (FCT) for all generated flows.

    Average FCT for Mice Flows.

    Average FCT for Elephant Flows.
