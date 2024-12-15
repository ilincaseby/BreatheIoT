import 'dart:io';
import 'dart:async'; // Adăugăm importul pentru Timer
import 'dart:convert'; // Pentru jsonDecode

import 'package:flutter/material.dart';
import 'package:mqtt_client/mqtt_client.dart' as mqtt;
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:mqtt_client/mqtt_server_client.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: const HomePage(),
      routes: {
        '/data': (context) => const DataPage(),
        '/commands': (context) => CommandsPage(),
      },
    );
  }
}

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          "BreatheIoT",
          selectionColor: Color.fromARGB(255, 105, 48, 66),
        ),
        backgroundColor: const Color.fromARGB(255, 14, 95, 81),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: () {
                Navigator.pushNamed(context, '/data');
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color.fromARGB(255, 57, 189, 1),
              ),
              child: const Text("Check Air Purifier Data"),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                Navigator.pushNamed(context, '/commands');
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color.fromARGB(255, 57, 189, 1),
              ),
              child: const Text("Send Commands"),
            ),
          ],
        ),
      ),
    );
  }
}

// class DataPage extends StatelessWidget {
//   const DataPage({super.key});

//   @override
//   Widget build(BuildContext context) {
//     return Scaffold(
//       appBar: AppBar(
//         title: const Text("Datele purificatorului"),
//         backgroundColor: const Color.fromARGB(255, 6, 51, 157),
//       ),
//       body: Center(
//         child: const Text(
//           "Aici vor fi afișate datele despre purificator.",
//           style: TextStyle(fontSize: 18),
//         ),
//       ),
//     );
//   }
// }

class DataPage extends StatefulWidget {
  const DataPage({super.key});

  @override
  _DataPageState createState() => _DataPageState();
}

class _DataPageState extends State<DataPage> {
  String data = "Aici vor fi afișate datele despre purificator.";
  Timer? _timer;

  @override
  void initState() {
    super.initState();
    fetchData();
    _timer = Timer.periodic(Duration(seconds: 3), (timer) {
      if (mounted) {
        // Verificăm dacă widget-ul este încă montat
        fetchData();
      } else {
        _timer?.cancel(); // Oprim Timer-ul dacă widget-ul nu mai este montat
      }
    });
  }

  @override
  void dispose() {
    _timer?.cancel(); // Oprește Timer-ul pentru a preveni eroarea
    super.dispose();
  }

  Future<void> fetchData() async {
    if (!mounted) return;
    const String url =
        "https://api.thingspeak.com/channels/2781680/feeds.json?api_key=MH3F3VO4BK16MLQK&results=1";

    try {
      final response = await http.get(Uri.parse(url));
      if (response.statusCode == 200) {
        // Decodăm răspunsul JSON
        var jsonResponse = jsonDecode(response.body);
        var feeds = jsonResponse['feeds'];

        // Afișăm valorile pentru toate câmpurile cu newline
        String formattedData = '';
        for (var feed in feeds) {
          formattedData += "Temperature: ${feed['field1']}\n\n\n\n";
          formattedData += "AQI: ${feed['field2']}\n\n\n\n";
          formattedData += "Filter left time: ${feed['field3']}\n\n\n\n";
          formattedData += "Humidity: ${feed['field4']}\n\n\n\n";
          formattedData += "Filter life remaining: ${feed['field5']}\n\n\n\n";
          formattedData += "Motor speed: ${feed['field6']}\n\n\n\n";
          formattedData += "Purify volume: ${feed['field7']}\n\n\n\n";
          formattedData += "Child lock: ${feed['field8']}\n\n\n\n";
        }

        setState(() {
          data = formattedData; // Afișează datele formatate
        });
      } else {
        setState(() {
          data = "Eroare: ${response.statusCode}";
        });
      }
    } catch (e) {
      setState(() {
        data = "Eroare la conectarea cu serverul: $e";
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Air Purifier Data 🍃"),
        backgroundColor: const Color.fromARGB(255, 6, 51, 157),
      ),
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(16),
          child: Text(
            data,
            style: const TextStyle(fontSize: 16),
          ),
        ),
      ),
    );
  }
}

class CommandsPage extends StatelessWidget {
  CommandsPage({super.key});

  final MqttServerClient client = MqttServerClient(
      '379c82a6c6934b6db7eb23e46479c875.s1.eu.hivemq.cloud', 'flutter_app');

  @override
  Widget build(BuildContext context) {
    client.onConnected = _onConnect;
    client.onDisconnected = _onDisconnect;
    client.port = 8883;
    client.setProtocolV311();
    client.secure = true;
    client.connect('sebastian', 'Sebi1406');
    return Scaffold(
      appBar: AppBar(
        title: const Text("Air Purifier Commands🤖"),
        backgroundColor: const Color.fromARGB(255, 14, 95, 81),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: () {
                // Comandă pentru a opri purificatorul
                print("Turn off air purifier");
                _sendCommand(1);
              },
              child: const Text("Turn off air purifier"),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                // Comandă pentru a porni purificatorul
                print("Turn on air purifier");
                _sendCommand(2);
              },
              child: const Text("Turn on air purifier"),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                // Comandă pentru a seta modul automat
                print("Set auto mode");
                _sendCommand(3);
              },
              child: const Text("Set auto mode"),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                // Comandă pentru a seta modul ventilator
                print("Set fan mode");
                _sendCommand(4);
              },
              child: const Text("Set fan mode"),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                // Comandă pentru a seta modul favorit
                print("Set favorite mode");
                _sendCommand(5);
              },
              child: const Text("Set favorite mode"),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                // Comandă pentru a seta modul silențios
                print("Set silent mode");
                _sendCommand(6);
              },
              child: const Text("Set silent mode"),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                // Comandă pentru a opri ionizatorul
                print("Set anion off");
                _sendCommand(7);
              },
              child: const Text("Set anion off"),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                // Comandă pentru a porni ionizatorul
                print("Set anion on");
                _sendCommand(8);
              },
              child: const Text("Set anion on"),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                // Comandă pentru a activa blocarea pentru copii
                print("Set child lock on");
                _sendCommand(9);
              },
              child: const Text("Set child lock on"),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                // Comandă pentru a dezactiva blocarea pentru copii
                print("Set child lock off");
                _sendCommand(10);
              },
              child: const Text("Set child lock off"),
            ),
          ],
        ),
      ),
    );
  }

  void _sendCommand(int commandNumber) {
    String message = '';

    // Determină mesajul pe care îl vei trimite pe baza numărului
    switch (commandNumber) {
      case 1:
        message = "turn_off_airp";
        break;
      case 2:
        message = "turn_on_airp";
        break;
      case 3:
        message = "set_auto_mode";
        break;
      case 4:
        message = "set_fan_mode";
        break;
      case 5:
        message = "set_favorite_mode";
        break;
      case 6:
        message = "set_silent_mode";
        break;
      case 7:
        message = "set_anion_off";
        break;
      case 8:
        message = "set_anion";
        break;
      case 9:
        message = "set_child_lock";
        break;
      case 10:
        message = "set_child_lock_off";
        break;
      default:
        message = "Unknown command";
    }

    // Trimite mesajul pe topicul corespunzător
    final mqtt.MqttClientPayloadBuilder builder =
        mqtt.MqttClientPayloadBuilder();
    builder.addString(message);

    // Alege topicul și trimite mesajul
    client.publishMessage(
        'commands', mqtt.MqttQos.atLeastOnce, builder.payload!);
  }

  // Funcția de conectare la broker
  void _onConnect() {
    print('Connected to MQTT broker');
  }

  // Funcția de deconectare de la broker
  void _onDisconnect() {
    print('Disconnected from MQTT broker');
  }
}
