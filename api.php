<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

$dataFile = 'data.json';
$targetUrl = 'https://mackrosophta.netlify.app'; // Hardcoded URL to open
$openInterval = 1; // Seconds between openings

// Initialize data file
if (!file_exists($dataFile)) {
    file_put_contents($dataFile, json_encode([
        'running' => false,
        'url' => $targetUrl,
        'interval' => $openInterval,
        'last_opened' => null
    ]));
}

// Handle start request
if ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['start'])) {
    $data = json_decode(file_get_contents($dataFile), true);
    $data['running'] = true;
    $data['last_opened'] = time();
    file_put_contents($dataFile, json_encode($data));
    
    echo json_encode([
        'status' => 'success',
        'message' => 'URL loop started',
        'url' => $data['url'],
        'interval' => $data['interval']
    ]);
    exit;
}

// Handle stop request
if ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['stop'])) {
    $data = json_decode(file_get_contents($dataFile), true);
    $data['running'] = false;
    file_put_contents($dataFile, json_encode($data));
    echo json_encode(['status' => 'success', 'message' => 'URL loop stopped']);
    exit;
}

// Handle status check
if ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['status'])) {
    $data = json_decode(file_get_contents($dataFile), true);
    echo json_encode($data);
    exit;
}

// Default response
echo json_encode(['status' => 'error', 'message' => 'Invalid request']);
?>