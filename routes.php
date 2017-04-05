<?php
// Routes

// README: When creating new functionality, create a new file for its routes
// To access the database, just type 'db', literally nothing else is needed

$app->get('/[{name}]', function ($request, $response, $args) {
    // Sample log message
    $this->logger->info("Slim-Skeleton '/' route");

    // Render index view
    return $this->renderer->render($response, 'index.phtml', $args);
});
