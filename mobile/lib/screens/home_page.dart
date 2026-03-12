import 'package:flutter/material.dart';
import '../services/auth_service.dart';
import 'login_page.dart';
import 'mood_page.dart';
import 'statistics_page.dart';
import 'mood_calender_page.dart';


class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    final authService = AuthService();
    final user = authService.currentUser;

    return Scaffold(
      appBar: AppBar(
        title: const Text("EmoLens"),
        centerTitle: true,
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () async {
              await authService.logout();

              Navigator.pushAndRemoveUntil(
                context,
                MaterialPageRoute(
                  builder: (_) => const LoginPage(),
                ),
                (route) => false,
              );
            },
          )
        ],
      ),
      body: Center(
        child: user != null
            ? Padding(
                padding: const EdgeInsets.all(24),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Icon(Icons.person, size: 80),
                    const SizedBox(height: 20),

                    const Text(
                      "Login sebagai:",
                      style: TextStyle(fontSize: 18),
                    ),

                    const SizedBox(height: 10),

                    Text(
                      user.email ?? "-",
                      style: const TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                      ),
                    ),

                    const SizedBox(height: 40),

                    /// BUTTON INPUT MOOD
                    SizedBox(
                      width: double.infinity,
                      child: ElevatedButton(
                        onPressed: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) => const MoodPage(),
                            ),
                          );
                        },
                        child: const Text("Input Mood"),
                      ),
                    ),

                    const SizedBox(height: 15),

                    /// BUTTON HISTORY
                    SizedBox(
                      width: double.infinity,
                      child: ElevatedButton(
                        onPressed: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) => const MoodCalendarPage(),
                            ),
                          );
                        },
                        child: const Text("Lihat Riwayat Mood"),
                      ),
                    ),

                    const SizedBox(height: 15),

                    /// BUTTON STATISTIK (FITUR 2)
                    SizedBox(
                      width: double.infinity,
                      child: ElevatedButton(
                        onPressed: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) => const StatisticsPage(),
                            ),
                          );
                        },
                        child: const Text("Lihat Statistik Mood"),
                      ),
                    ),
                  ],
                ),
              )
            : const Text("User tidak ditemukan"),
      ),
    );
  }
}