<?php

use Illuminate\Support\Facades\Route;
use Kreait\Firebase\Factory;

Route::get('/', function () {
    return view('welcome');
});

/*
|---------------------------------------
| Test koneksi Firebase
|---------------------------------------
*/

Route::get('/firebase-test', function () {

    $factory = (new Factory)
        ->withServiceAccount(storage_path('app/firebase/firebase_credentials.json'))
        ->withDatabaseUri(env('FIREBASE_DATABASE_URL'));

    $database = $factory->createDatabase();

    return "Firebase connected!";
});

/*
|---------------------------------------
| Kirim data ke Firebase
|---------------------------------------
*/

Route::get('/kirim-data', function () {

    $factory = (new Factory)
        ->withServiceAccount(storage_path('app/firebase/firebase_credentials.json'))
        ->withDatabaseUri(env('FIREBASE_DATABASE_URL'));

    $database = $factory->createDatabase();

    $database->getReference('users')->push([
        'nama' => 'Joy',
        'email' => 'joy@gmail.com'
    ]);

    return "Data berhasil dikirim ke Firebase!";
});