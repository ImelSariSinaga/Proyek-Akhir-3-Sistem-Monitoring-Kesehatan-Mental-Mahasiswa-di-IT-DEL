import 'package:flutter/material.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:fl_chart/fl_chart.dart';

class StatisticsPage extends StatelessWidget {
  const StatisticsPage({super.key});

  @override
  Widget build(BuildContext context) {
    final user = FirebaseAuth.instance.currentUser;

    return Scaffold(
      appBar: AppBar(
        title: const Text("Statistik Mood"),
        centerTitle: true,
      ),
      body: StreamBuilder<QuerySnapshot>(
        stream: FirebaseFirestore.instance
            .collection('moods')
            .where('userId', isEqualTo: user!.uid)
            .snapshots(),
        builder: (context, snapshot) {
          if (!snapshot.hasData) {
            return const Center(child: CircularProgressIndicator());
          }

          final docs = snapshot.data!.docs;

          Map<String, int> moodCount = {
            "senang": 0,
            "marah": 0,
            "sedih": 0,
            "takut": 0,
            "biasa": 0,
            "kaget": 0,
            "jijik": 0,
          };

          for (var doc in docs) {
            String mood = doc['mood'];
            if (moodCount.containsKey(mood)) {
              moodCount[mood] = moodCount[mood]! + 1;
            }
          }

          return Padding(
            padding: const EdgeInsets.all(16),
            child: PieChart(
              PieChartData(
                sections: moodCount.entries.map((entry) {
                  return PieChartSectionData(
                    value: entry.value.toDouble(),
                    title: entry.key,
                  );
                }).toList(),
              ),
            ),
          );
        },
      ),
    );
  }
}