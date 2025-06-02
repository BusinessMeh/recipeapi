<?php
header('Content-Type: application/json');

// CORS headers - adjust these as needed
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

// Handle preflight requests
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    exit(0);
}

$dataFile = 'data.json';
$targetUrl = 'https://mackrosophta.netlify.app'; // Your target URL
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

// Handle requests
$request = $_SERVER['REQUEST_URI'];
$method = $_SERVER['REQUEST_METHOD'];

// Route requests
switch (true) {
    case strpos($request, '/api.php/status') !== false:
        $data = json_decode(file_get_contents($dataFile), true);
        echo json_encode($data);
        break;
        
    case strpos($request, '/api.php/start') !== false && $method === 'GET':
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
        break;
        
    case strpos($request, '/api.php/stop') !== false && $method === 'GET':
        $data = json_decode(file_get_contents($dataFile), true);
        $data['running'] = false;
        file_put_contents($dataFile, json_encode($data));
        echo json_encode(['status' => 'success', 'message' => 'URL loop stopped']);
        break;
        
    default:
        http_response_code(404);
        echo json_encode(['status' => 'error', 'message' => 'Endpoint not found']);
        break;
}
?>