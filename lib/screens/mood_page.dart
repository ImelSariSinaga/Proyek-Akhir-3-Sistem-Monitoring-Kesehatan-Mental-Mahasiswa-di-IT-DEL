import 'package:emolens_app/screens/mood_calender_page.dart';
import 'package:flutter/material.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';


class MoodPage extends StatefulWidget {
  const MoodPage({super.key});

  @override
  State<MoodPage> createState() => _MoodPageState();
}

class _MoodPageState extends State<MoodPage> {

  String selectedMood = "senang";
  final TextEditingController noteController = TextEditingController();
  bool isLoading = false;

  // 🔥 Mapping Mood → Code (Untuk AI)
  final Map<String, int> moodCodeMap = {
    "senang": 1,
    "marah": 2,
    "sedih": 3,
    "takut": 4,
    "biasa": 5,
    "kaget": 6,
    "jijik": 7,
  };

  Future<void> saveMood() async {
    final user = FirebaseAuth.instance.currentUser;

    if (user == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("User belum login")),
      );
      return;
    }

    try {
      setState(() {
        isLoading = true;
      });

      int moodCode = moodCodeMap[selectedMood] ?? 0;

      await FirebaseFirestore.instance.collection('moods').add({
        'userId': user.uid,
        'email': user.email,
        'mood_label': selectedMood,   // Untuk UI
        'emosi_kode': moodCode,        // Untuk AI
        'note': noteController.text,
        'createdAt': Timestamp.now(),
      });

      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Mood berhasil disimpan ✅")),
      );

      noteController.clear();

    } catch (e) {
      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Gagal menyimpan mood: $e")),
      );

      print("FIRESTORE ERROR: $e");
    } finally {
      if (mounted) {
        setState(() {
          isLoading = false;
        });
      }
    }
  }

  @override
  void dispose() {
    noteController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Input Mood"),
        centerTitle: true,
      ),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              "Bagaimana perasaanmu hari ini?",
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),

            const SizedBox(height: 20),

            DropdownButtonFormField<String>(
              value: selectedMood,
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
              ),
              items: const [
                DropdownMenuItem(value: "senang", child: Text("Senang 😊")),
                DropdownMenuItem(value: "marah", child: Text("Marah 😡")),
                DropdownMenuItem(value: "sedih", child: Text("Sedih 😢")),
                DropdownMenuItem(value: "takut", child: Text("Takut 😰")),
                DropdownMenuItem(value: "biasa", child: Text("Biasa 😐")),
                DropdownMenuItem(value: "kaget", child: Text("Kaget 😱")),
                DropdownMenuItem(value: "jijik", child: Text("Jijik 🤢")),
              ],
              onChanged: (value) {
                setState(() {
                  selectedMood = value!;
                });
              },
            ),

            const SizedBox(height: 15),

            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => const MoodCalendarPage(),
                  ),
                );
              },
              child: const Text("Lihat Riwayat Mood"),
            ),

            const SizedBox(height: 20),

            TextField(
              controller: noteController,
              maxLines: 3,
              decoration: const InputDecoration(
                labelText: "Catatan (opsional)",
                border: OutlineInputBorder(),
              ),
            ),

            const SizedBox(height: 30),

            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: isLoading ? null : saveMood,
                child: isLoading
                    ? const CircularProgressIndicator(color: Colors.white)
                    : const Text("Simpan Mood"),
              ),
            ),
          ],
        ),
      ),
    );
  }
}