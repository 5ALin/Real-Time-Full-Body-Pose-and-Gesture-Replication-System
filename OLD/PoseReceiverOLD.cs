using System;
using System.IO;
using System.Net.Sockets;
using UnityEngine;

public class PoseReceiver : MonoBehaviour
{
    TcpClient client; // For connecting to Python
    StreamReader reader;

    void Start()
    {
        ConnectToServer();
    }

    void Update()
    {
        if (client != null && client.Connected)
        {
            try
            {
                // Read JSON data from Python
                string data = reader.ReadLine();
                if (!string.IsNullOrEmpty(data))
                {
                    ProcessData(data);
                }
            }
            catch (Exception e)
            {
                Debug.LogError("Error receiving data: " + e.Message);
            }
        }
    }

    void ConnectToServer()
    {
        try
        {
            client = new TcpClient("localhost", 12345); // Connect to Python on localhost:12345
            reader = new StreamReader(client.GetStream());
            Debug.Log("Connected to Python server!");
        }
        catch (Exception e)
        {
            Debug.LogError("Connection failed: " + e.Message);
        }
    }

    void ProcessData(string jsonData)
    {
        // Parse JSON data
        var landmarks = JsonUtility.FromJson<LandmarkData>(jsonData);
        
        // Example: Move model's head
        Transform head = transform.Find("Head");
        if (head != null)
        {
            head.localPosition = new Vector3(landmarks.head.x, landmarks.head.y, landmarks.head.z);
        }

        // Example: Move left and right hands
        Transform leftHand = transform.Find("LeftHand");
        Transform rightHand = transform.Find("RightHand");

        if (leftHand != null)
        {
            leftHand.localPosition = new Vector3(landmarks.left_hand.x, landmarks.left_hand.y, landmarks.left_hand.z);
        }

        if (rightHand != null)
        {
            rightHand.localPosition = new Vector3(landmarks.right_hand.x, landmarks.right_hand.y, landmarks.right_hand.z);
        }
    }

    private void OnApplicationQuit()
    {
        reader?.Close();
        client?.Close();
    }

    [Serializable]
    public class LandmarkData
    {
        public Landmark head;
        public Landmark left_hand;
        public Landmark right_hand;
    }

    [Serializable]
    public class Landmark
    {
        public float x;
        public float y;
        public float z;
    }
}
