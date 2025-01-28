using UnityEngine;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System;
using UnityEngine.UI;

public class PoseReceiver : MonoBehaviour
{
    private UdpClient udpClient;
    private Thread receiveThread;
    private string host = "127.0.0.1";
    private int port = 12345;
    private float[] landmarkPositions = new float[99]; // 33 landmarks * 3 coordinates (x, y, z)
    private GameObject[] landmarkBalls = new GameObject[33]; // 33 balls for landmarks
    private LineRenderer[] lineRenderers; // To store LineRenderers for each connection

    // Define the actual MediaPipe POSE_CONNECTIONS between landmarks
    private readonly int[,] poseConnections = new int[,]
    {
        {8,6},{6,5},{5,4},{4,0},{0,1},{1,2},{2,3},{3,7},
        {10,9},
        {12,11},{11,23},{23,24},{24,12},
        {12,14},{14,16},
        {11,13},{13,15},
        {16,18},{18,20},{20,22},{16,20},
        {15,21},{21,19},{19,17},{15,19},
        {24,26},{26,28},
        {23,25},{25,27},
        {28,30},{30,32},{32,28},
        {27,29},{29,31},{31,27}
    };

    void Start()
    {
        // Start the UDP listener in a separate thread
        receiveThread = new Thread(new ThreadStart(ReceiveData));
        receiveThread.IsBackground = true;
        receiveThread.Start();

        // Initialize balls for landmarks
        landmarkBalls = new GameObject[33];
        for (int i = 0; i < 33; i++)
        {
            landmarkBalls[i] = GameObject.CreatePrimitive(PrimitiveType.Sphere);
            landmarkBalls[i].transform.localScale = new Vector3(0.05f, 0.05f, 0.05f);
            landmarkBalls[i].GetComponent<Renderer>().material.color = new Color(UnityEngine.Random.value, UnityEngine.Random.value, UnityEngine.Random.value);
        }

        // Initialize the LineRenderers for connections
        lineRenderers = new LineRenderer[poseConnections.GetLength(0)];
        for (int i = 0; i < poseConnections.GetLength(0); i++)
        {
            GameObject lineObj = new GameObject("Line" + i);
            LineRenderer lineRenderer = lineObj.AddComponent<LineRenderer>();
            lineRenderer.startWidth = 0.05f;
            lineRenderer.endWidth = 0.05f;
            lineRenderer.material = new Material(Shader.Find("Sprites/Default"));
            lineRenderers[i] = lineRenderer;
        }
    }

    private void ReceiveData()
    {
        udpClient = new UdpClient(port);
        while (true)
        {
            try
            {
                // Receive the byte data from Python
                IPEndPoint endPoint = new IPEndPoint(IPAddress.Parse(host), port);
                byte[] receivedBytes = udpClient.Receive(ref endPoint);

                // Convert the byte data to landmark positions
                for (int i = 0; i < 99; i++) // 33 landmarks * 3 coordinates (x, y, z)
                {
                    landmarkPositions[i] = BitConverter.ToSingle(receivedBytes, i * 4);
                }
            }
            catch (Exception e)
            {
                Debug.LogError("Error receiving data: " + e.Message);
            }
        }
    }

    void Update()
    {
        // Normalize the X, Y, Z coordinates for Unity's world space
        float xOffset = 5f; // Adjust this offset to move the landmarks into view
        float yOffset = 3f; // Adjust this offset for the Y-axis

        // Update the positions of the balls based on the received landmarks
        for (int i = 0; i < 33; i++)
        {
            // Create landmarks in Unity world space
            Vector3 newPos = new Vector3(landmarkPositions[i * 3] * xOffset, 
                                        landmarkPositions[i * 3 + 1] * yOffset, 
                                        landmarkPositions[i * 3 + 2]);

            // Apply the new position to the ball
            landmarkBalls[i].transform.position = newPos;
        }

        // Update the lines connecting the landmarks based on the pose connections
        for (int i = 0; i < poseConnections.GetLength(0); i++)
        {
            int startIdx = poseConnections[i, 0];
            int endIdx = poseConnections[i, 1];

            // Get the start and end points for the line
            Vector3 startPos = landmarkBalls[startIdx].transform.position;
            Vector3 endPos = landmarkBalls[endIdx].transform.position;

            // Set the positions for the line renderer
            lineRenderers[i].SetPosition(0, startPos);
            lineRenderers[i].SetPosition(1, endPos);
        }
    }

    void OnApplicationQuit()
    {
        if (receiveThread != null && receiveThread.IsAlive)
        {
            receiveThread.Abort();
        }
    }
}
