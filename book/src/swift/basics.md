# Swift Language Basics

> Master Swift fundamentals with hands-on examples and real-world applications

## 🎯 Learning Objectives

By the end of this chapter, you'll be able to:
- Write clean, idiomatic Swift code
- Understand Swift's type system and memory management
- Use optionals safely and effectively
- Apply Swift's modern features in real projects

## 📝 Variables and Constants

### The `let` vs `var` Decision Tree

```swift
// Use 'let' by default - Swift encourages immutability
let appName = "MyApp"           // ✅ Won't change
let maxRetries = 3              // ✅ Configuration constant
let userID = UUID()             // ✅ Generated once

// Use 'var' only when you need to modify
var currentScore = 0            // ✅ Will change during game
var isLoading = false           // ✅ State that toggles
var items: [String] = []        // ✅ Collection that grows
```

### Type Inference vs Explicit Types

```swift
// Swift infers types intelligently
let message = "Hello, World!"              // String
let count = 42                             // Int
let price = 19.99                          // Double
let isActive = true                        // Bool

// Be explicit when needed for clarity
let timeout: TimeInterval = 30.0           // More descriptive than Double
let userAge: Int8 = 25                     // Specific integer size
let coordinates: (Double, Double) = (0, 0) // Tuple type
```

## 🔢 Swift's Type System

### Numeric Types - Choose Wisely

```swift
// Default integer type
let regularNumber = 100                    // Int (64-bit on modern devices)

// Specific sizes when memory matters
let smallValue: Int8 = 127                 // -128 to 127
let mediumValue: Int16 = 32767             // -32,768 to 32,767
let largeValue: Int64 = 9223372036854775807

// Unsigned when you need only positive values
let arrayIndex: UInt = 5                   // 0 to max positive
let colorComponent: UInt8 = 255            // RGB values (0-255)

// Floating point precision
let roughCalculation: Float = 3.14159      // 32-bit, ~6 decimal digits
let preciseCalculation: Double = 3.14159265359 // 64-bit, ~15 decimal digits
```

### String Manipulation - Modern Swift Way

```swift
// String interpolation (preferred over concatenation)
let name = "Alice"
let age = 30
let greeting = "Hello, \(name)! You are \(age) years old."

// Multi-line strings
let poem = """
    Roses are red,
    Violets are blue,
    Swift is awesome,
    And so are you!
    """

// String methods you'll use daily
let email = "  user@example.com  "
let cleanEmail = email.trimmingCharacters(in: .whitespacesAndNewlines)
let isValidEmail = cleanEmail.contains("@") && cleanEmail.contains(".")

// String formatting for UI
let formattedPrice = String(format: "%.2f", 29.99)  // "29.99"
let paddedNumber = String(format: "%03d", 7)        // "007"
```

## ❓ Optionals - Swift's Safety Net

### Understanding Optionals

```swift
// Optionals represent "might have a value, might not"
var userName: String? = nil                // No value yet
userName = "john_doe"                      // Now has a value

// Dictionary lookups return optionals
let userAges = ["Alice": 30, "Bob": 25]
let aliceAge = userAges["Alice"]           // Optional(30)
let charlieAge = userAges["Charlie"]       // nil
```

### Safe Unwrapping Techniques

```swift
// 1. Optional binding (if let) - Most common
if let age = userAges["Alice"] {
    print("Alice is \(age) years old")
} else {
    print("Alice's age is unknown")
}

// 2. Guard statements - Early exit pattern
func processUser(name: String?) {
    guard let userName = name else {
        print("Invalid user name")
        return
    }
    
    // userName is safely unwrapped here
    print("Processing user: \(userName)")
}

// 3. Nil coalescing - Provide defaults
let displayName = userName ?? "Guest"
let itemCount = items.count > 0 ? items.count : 0

// 4. Optional chaining - Safe property access
struct User {
    let profile: Profile?
}

struct Profile {
    let avatar: String?
}

let user = User(profile: Profile(avatar: "avatar.jpg"))
let avatarURL = user.profile?.avatar ?? "default.jpg"
```

### When NOT to Force Unwrap

```swift
// ❌ Dangerous - will crash if nil
let forcedAge = userAges["Charlie"]!       // Runtime crash!

// ✅ Safe alternatives
let safeAge = userAges["Charlie"] ?? 0     // Default value
if let age = userAges["Charlie"] {         // Optional binding
    // Use age safely
}

// ⚠️ Force unwrapping is OK only when you're 100% certain
let url = URL(string: "https://apple.com")! // URL is valid
```

## 🏗️ Functions - Building Blocks

### Function Syntax and Best Practices

```swift
// Basic function with clear parameter names
func calculateTip(billAmount: Double, tipPercentage: Double) -> Double {
    return billAmount * (tipPercentage / 100)
}

// External and internal parameter names
func send(message: String, to recipient: String) {
    print("Sending '\(message)' to \(recipient)")
}

// Usage reads like English
send(message: "Hello!", to: "Alice")

// Default parameters
func createUser(name: String, age: Int = 18, isActive: Bool = true) -> User {
    return User(name: name, age: age, isActive: isActive)
}

// Multiple ways to call
let user1 = createUser(name: "Alice")
let user2 = createUser(name: "Bob", age: 25)
let user3 = createUser(name: "Charlie", age: 30, isActive: false)
```

### Advanced Function Features

```swift
// Variadic parameters
func average(of numbers: Double...) -> Double {
    let sum = numbers.reduce(0, +)
    return sum / Double(numbers.count)
}

let avg = average(of: 1.0, 2.0, 3.0, 4.0, 5.0)

// In-out parameters (modify the original)
func swapValues<T>(_ a: inout T, _ b: inout T) {
    let temp = a
    a = b
    b = temp
}

var x = 5
var y = 10
swapValues(&x, &y)  // x is now 10, y is now 5

// Functions as first-class citizens
func applyOperation(_ a: Int, _ b: Int, operation: (Int, Int) -> Int) -> Int {
    return operation(a, b)
}

let result = applyOperation(5, 3, operation: +)  // 8
```

## 🎮 Control Flow

### Conditional Statements

```swift
// Traditional if-else
let temperature = 75
if temperature > 80 {
    print("It's hot!")
} else if temperature > 60 {
    print("It's warm")
} else {
    print("It's cool")
}

// Switch statements - Powerful pattern matching
let grade = "A"
switch grade {
case "A", "A+":
    print("Excellent!")
case "B", "B+":
    print("Good job!")
case "C":
    print("Average")
default:
    print("Needs improvement")
}

// Switch with ranges
let score = 85
switch score {
case 90...100:
    print("A grade")
case 80..<90:
    print("B grade")
case 70..<80:
    print("C grade")
default:
    print("Below C")
}
```

### Loops and Iteration

```swift
// For-in loops (most common)
let fruits = ["apple", "banana", "orange"]
for fruit in fruits {
    print("I like \(fruit)")
}

// With indices when needed
for (index, fruit) in fruits.enumerated() {
    print("\(index + 1). \(fruit)")
}

// Range-based loops
for i in 1...5 {
    print("Count: \(i)")
}

// While loops for unknown iterations
var attempts = 0
while attempts < 3 {
    print("Attempt \(attempts + 1)")
    attempts += 1
}

// Repeat-while (do-while equivalent)
var input: String
repeat {
    input = readLine() ?? ""
} while input.isEmpty
```

## 🧮 Collections

### Arrays - Ordered Collections

```swift
// Creating arrays
var numbers: [Int] = []                    // Empty array
var colors = ["red", "green", "blue"]      // Array literal
var scores = Array(repeating: 0, count: 5) // [0, 0, 0, 0, 0]

// Common operations
colors.append("yellow")                     // Add to end
colors.insert("purple", at: 1)             // Insert at index
colors.remove(at: 0)                       // Remove by index
colors.removeAll { $0.hasPrefix("g") }     // Remove matching elements

// Useful array methods
let evenNumbers = numbers.filter { $0 % 2 == 0 }
let doubled = numbers.map { $0 * 2 }
let sum = numbers.reduce(0, +)
let hasLargeNumber = numbers.contains { $0 > 100 }
```

### Dictionaries - Key-Value Storage

```swift
// Creating dictionaries
var userScores: [String: Int] = [:]
var capitals = [
    "France": "Paris",
    "Japan": "Tokyo",
    "Brazil": "Brasília"
]

// Safe access with optionals
if let capital = capitals["France"] {
    print("Capital of France is \(capital)")
}

// Updating values
capitals["Germany"] = "Berlin"              // Add new
capitals["Japan"] = "Tokyo"                 // Update existing
capitals.removeValue(forKey: "Brazil")      // Remove

// Iterating over dictionaries
for (country, capital) in capitals {
    print("\(capital) is the capital of \(country)")
}
```

### Sets - Unique Collections

```swift
// Creating sets
var uniqueNumbers: Set<Int> = []
var vowels: Set<Character> = ["a", "e", "i", "o", "u"]

// Set operations
let setA: Set = [1, 2, 3, 4]
let setB: Set = [3, 4, 5, 6]

let union = setA.union(setB)               // [1, 2, 3, 4, 5, 6]
let intersection = setA.intersection(setB)  // [3, 4]
let difference = setA.subtracting(setB)     // [1, 2]
```

## 🎯 Real-World Example: Todo App Model

```swift
import Foundation

// Enum for task priority
enum Priority: String, CaseIterable {
    case low = "Low"
    case medium = "Medium"
    case high = "High"
    
    var color: String {
        switch self {
        case .low: return "green"
        case .medium: return "orange"
        case .high: return "red"
        }
    }
}

// Task model
struct Task {
    let id = UUID()
    var title: String
    var isCompleted: Bool = false
    var priority: Priority = .medium
    let createdAt = Date()
    var dueDate: Date?
    
    // Computed property
    var isOverdue: Bool {
        guard let dueDate = dueDate else { return false }
        return !isCompleted && dueDate < Date()
    }
    
    // Method to toggle completion
    mutating func toggleCompletion() {
        isCompleted.toggle()
    }
}

// Todo manager
class TodoManager {
    private var tasks: [Task] = []
    
    func addTask(title: String, priority: Priority = .medium, dueDate: Date? = nil) {
        let task = Task(title: title, priority: priority, dueDate: dueDate)
        tasks.append(task)
    }
    
    func completeTask(withId id: UUID) {
        if let index = tasks.firstIndex(where: { $0.id == id }) {
            tasks[index].toggleCompletion()
        }
    }
    
    func deleteTask(withId id: UUID) {
        tasks.removeAll { $0.id == id }
    }
    
    // Computed properties for different views
    var completedTasks: [Task] {
        tasks.filter { $0.isCompleted }
    }
    
    var pendingTasks: [Task] {
        tasks.filter { !$0.isCompleted }
    }
    
    var overdueTasks: [Task] {
        tasks.filter { $0.isOverdue }
    }
    
    var highPriorityTasks: [Task] {
        tasks.filter { $0.priority == .high && !$0.isCompleted }
    }
}

// Usage example
let todoManager = TodoManager()
todoManager.addTask(title: "Learn Swift", priority: .high)
todoManager.addTask(title: "Build an app", priority: .medium, dueDate: Date().addingTimeInterval(86400 * 7))
todoManager.addTask(title: "Submit to App Store", priority: .high, dueDate: Date().addingTimeInterval(86400 * 30))

print("High priority tasks: \(todoManager.highPriorityTasks.count)")
print("Overdue tasks: \(todoManager.overdueTasks.count)")
```

## 🔍 Common Patterns and Idioms

### Error Handling Preview

```swift
enum ValidationError: Error {
    case emptyTitle
    case titleTooLong
    case invalidEmail
}

func validateTask(title: String, email: String?) throws -> Bool {
    guard !title.isEmpty else {
        throw ValidationError.emptyTitle
    }
    
    guard title.count <= 100 else {
        throw ValidationError.titleTooLong
    }
    
    if let email = email {
        guard email.contains("@") else {
            throw ValidationError.invalidEmail
        }
    }
    
    return true
}

// Usage with do-catch
do {
    try validateTask(title: "Learn Swift", email: "user@example.com")
    print("Task is valid!")
} catch ValidationError.emptyTitle {
    print("Title cannot be empty")
} catch ValidationError.titleTooLong {
    print("Title is too long")
} catch {
    print("Validation failed: \(error)")
}
```

## 🎯 Practice Exercises

### Exercise 1: Grade Calculator
```swift
// Create a function that calculates letter grade from percentage
func calculateGrade(percentage: Double) -> String {
    // Your implementation here
    switch percentage {
    case 90...100: return "A"
    case 80..<90: return "B"
    case 70..<80: return "C"
    case 60..<70: return "D"
    default: return "F"
    }
}

// Test cases
assert(calculateGrade(percentage: 95) == "A")
assert(calculateGrade(percentage: 85) == "B")
assert(calculateGrade(percentage: 55) == "F")
```

### Exercise 2: Word Counter
```swift
// Count word frequency in a text
func wordFrequency(in text: String) -> [String: Int] {
    let words = text.lowercased()
        .components(separatedBy: .punctuationCharacters)
        .joined()
        .components(separatedBy: .whitespacesAndNewlines)
        .filter { !$0.isEmpty }
    
    var frequency: [String: Int] = [:]
    for word in words {
        frequency[word, default: 0] += 1
    }
    
    return frequency
}

// Test
let text = "Swift is great. Swift is powerful. Swift is fun!"
let result = wordFrequency(in: text)
print(result) // ["swift": 3, "is": 3, "great": 1, "powerful": 1, "fun": 1]
```

## 📚 Key Takeaways

1. **Prefer `let` over `var`** - Immutability makes code safer and more predictable
2. **Use optionals safely** - Never force unwrap unless you're absolutely certain
3. **Leverage type inference** - Let Swift figure out types when it's clear
4. **Write descriptive function names** - Code should read like English
5. **Use collections appropriately** - Arrays for order, Sets for uniqueness, Dictionaries for lookup
6. **Handle errors gracefully** - Use Swift's error handling system

## 🔗 What's Next?

In the next chapter, we'll explore **Collections & Control Flow** in depth, learning advanced array operations, functional programming concepts, and complex control flow patterns.

---

*Practice these concepts in Swift Playgrounds or Xcode to reinforce your learning!*
