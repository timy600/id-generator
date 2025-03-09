
# Identity Service - Proposed Solution

## Overview
This document outlines the proposed solution for the Identity Service, which generates human-readable 7-letter IDs using a set of 34 characters (digits and alphabets excluding 'I' and 'O'). The service was designed to handle bulk generation, concurrency, persistence, fault tolerance, and performance considerations.

## Solution Approach
Three potential approaches were considered for generating unique IDs:

1. **Pure Randomness:** Using `random.choices()` to generate IDs randomly.
2. **SQLite Database:** Storing generated IDs in a database to ensure uniqueness.
3. **Sequential with a Counter:** Maintaining a counter to generate sequential unique IDs.

After analysis, the sequential counter approach was chosen, implemented in a hybrid system leveraging batching and threading to optimize efficiency.

## Implementation Details

### **1. Class-Based Design**
The ID generation logic was encapsulated within the `IDGenerator` class. This design allows configurability based on the specific use case, such as performance testing, crash recovery, and real-world counter implementation.

### **2. Handling Bulk Generation**
The bulk generation function was tested and optimized to ensure uniqueness and efficient formatting.

### **3. Concurrency Handling**
The solution was designed to handle multiple concurrent requests using threading, ensuring thread safety while maintaining performance.

### **4. Persistence and Fault Tolerance**
The service ensures persistence by saving the counter state upon exit using:
```python
import atexit
atexit.register(self._save_counter_on_exit)
```
This prevents ID duplication upon restarts.

### **5. Performance Considerations**
- A simplified 8-letter base encoding was used for performance testing.
- The counter was managed in a way that minimized I/O overhead, with batch of 1000 IDs before rewriting.

### **6. Approaching the end of the Sequence**
When hitting the last decile of the possible permutations, an alert-message is sent.

### **7. Reaching the end of the Sequence**
I implemented a separate class for handling the sequence exhaustion by adding the possible letters, among them the I and O missing from the original 34 base encoding.
```python
ID_CHARACTERS_EXTRA = "IOÀÈÉÔÖ"
```

### **8. Separate IRL counter from testings**
The unit tests are setup with their own counter so that it wouldnt affect the real life service usage.


## Key Challenges & Insights
1. **Random Generation Pitfalls:**
   - Despite the high theoretical number of permutations (~52 billion), testing bulk generation (2 million samples) resulted in duplicate occurrences much more frequently than expected.
   - Probability calculations confirmed the issue:
   ```python
   proba_not_one_turn = 1 - 1/permutations
   proba_at_least_once_in_x_turn = 1 - (proba_not_one_turn)**1_000_000
   print(proba_at_least_once_in_x_turn)  # ~0.00002
   ```
   - This reduced confidence in a purely random approach.

2. **SQLite Performance Issues:**
   - Initial attempts at using an SQLite database were abandoned due to significant performance overhead.

3. **Crashing Test Failures:**
   - Early versions of the implementation failed the crash recovery tests. After revisiting the counter-based approach, a persistent save mechanism was implemented, which resolved the issue.

4. **Handling Sequence Exhaustion:**
   - Two options were considered:
     1. Extending the length of the ID.
     2. Expanding the character set.
   - The second option was chosen and implemented as a separate class to maintain a clear distinction between configuration and generation logic.

## Conclusion
The final solution provides a robust and efficient approach to ID generation, balancing uniqueness, performance, and fault tolerance. The class-based architecture ensures modularity, making it adaptable to different testing scenarios and production use cases.

