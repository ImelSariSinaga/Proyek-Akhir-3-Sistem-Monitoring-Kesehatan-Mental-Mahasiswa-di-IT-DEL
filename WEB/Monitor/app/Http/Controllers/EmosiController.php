<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class EmosiController extends Controller
{
    public function index()
    {
        $database = app('firebase.database');
        $data = $database->getReference('moods')->getValue();

        $hasil = [];

        foreach ($data as $item) {

            // kirim ke AI python
            $response = Http::post('http://127.0.0.1:5000/analyze', [
                'note' => $item['note'],
                'userId' => $item['userId'],
                'emosi_kode' => $item['emosi_kode']
            ]);

            $ai = $response->json();

            $hasil[] = [
                'note' => $item['note'],
                'ringkasan' => $ai['ringkasan'] ?? '',
                'emosi' => $ai['emosi_terdeteksi'] ?? ''
            ];
        }

        return view('emosi', compact('hasil'));
    }
}