#include <SFML/Graphics.hpp>
#include <SFML/System/Vector3.hpp>
#include <cmath>
#include <vector>

const int WINDOW_WIDTH = 800;
const int WINDOW_HEIGHT = 600;
const float CUBE_SIZE = 100.0f;

// Function to project 3D points to 2D
sf::Vector2f project(const float x, const float y, const float z,
                     const float distance) {
  const float factor = distance / (distance + z);
  return sf::Vector2f(static_cast<float>(WINDOW_WIDTH) / 2 + x * factor,
                      static_cast<float>(WINDOW_HEIGHT) / 2 - y * factor);
}

// Function to rotate a point in 3D space
sf::Vector3f rotate(const sf::Vector3f vec, const float angleX,
                    const float angleY, const float angleZ) {
  // Rotate around X axis
  const float cosX = cos(angleX), sinX = sin(angleX);
  const float y1 = vec.y * cosX - vec.z * sinX;
  const float z1 = vec.y * sinX + vec.z * cosX;

  // Rotate around Y axis
  const float cosY = cos(angleY), sinY = sin(angleY);
  const float x2 = vec.x * cosY + z1 * sinY;
  const float z2 = -vec.x * sinY + z1 * cosY;

  // Rotate around Z axis
  const float cosZ = cos(angleZ), sinZ = sin(angleZ);
  const float x3 = x2 * cosZ - y1 * sinZ;
  const float y3 = x2 * sinZ + y1 * cosZ;

  return sf::Vector3f(x3, y3, z2);
}

int main() {
  sf::RenderWindow window(sf::VideoMode(WINDOW_WIDTH, WINDOW_HEIGHT),
                          "SFML App");
  window.setFramerateLimit(60);

  // Define the vertices of the cube
  const std::vector<sf::Vector3f> vertices = {
      {-CUBE_SIZE, -CUBE_SIZE, -CUBE_SIZE}, {CUBE_SIZE, -CUBE_SIZE, -CUBE_SIZE},
      {CUBE_SIZE, CUBE_SIZE, -CUBE_SIZE},   {-CUBE_SIZE, CUBE_SIZE, -CUBE_SIZE},
      {-CUBE_SIZE, -CUBE_SIZE, CUBE_SIZE},  {CUBE_SIZE, -CUBE_SIZE, CUBE_SIZE},
      {CUBE_SIZE, CUBE_SIZE, CUBE_SIZE},    {-CUBE_SIZE, CUBE_SIZE, CUBE_SIZE}};

  // Define the edges of the cube (pairs of vertex indices)
  const std::vector<std::pair<int, int>> edges = {
      {0, 1}, {1, 2}, {2, 3}, {3, 0}, {4, 5}, {5, 6},
      {6, 7}, {7, 4}, {0, 4}, {1, 5}, {2, 6}, {3, 7}};

  float angleX = 0, angleY = 0, angleZ = 0;
  const float angleSpeed = 0.01f;
  const float distance = 400.0f;

  while (window.isOpen()) {
    sf::Event event;
    while (window.pollEvent(event)) {
      if (event.type == sf::Event::Closed)
        window.close();
    }

    // Update rotation angles
    angleX += angleSpeed;
    angleY += angleSpeed;
    angleZ += angleSpeed;

    window.clear(sf::Color::Black);

    // Draw the cube
    for (const auto &edge : edges) {
      sf::Vector3f p1 = rotate(vertices[edge.first], angleX, angleY, angleZ);
      sf::Vector3f p2 = rotate(vertices[edge.second], angleX, angleY, angleZ);

      // Project the points to 2D
      sf::Vector2f projectedP1 = project(p1.x, p1.y, p1.z, distance);
      sf::Vector2f projectedP2 = project(p2.x, p2.y, p2.z, distance);

      sf::Vertex line[] = {sf::Vertex(projectedP1, sf::Color::White),
                           sf::Vertex(projectedP2, sf::Color::White)};

      window.draw(line, 2, sf::Lines);
    }

    window.display();
  }

  return 0;
}
