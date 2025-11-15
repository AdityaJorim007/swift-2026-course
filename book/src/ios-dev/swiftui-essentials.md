# SwiftUI Essentials

> Build modern iOS apps with declarative UI programming

## 🎯 Learning Objectives

Master SwiftUI fundamentals to create beautiful, responsive iOS applications:
- Understand declarative UI programming concepts
- Build complex layouts with stacks and containers
- Manage app state effectively
- Create reusable custom components
- Implement navigation and data flow

## 🏗️ SwiftUI Architecture

### Declarative vs Imperative UI

```swift
// ❌ Imperative (UIKit way)
let label = UILabel()
label.text = "Hello, World!"
label.textColor = .blue
label.font = UIFont.systemFont(ofSize: 24)
view.addSubview(label)

// ✅ Declarative (SwiftUI way)
Text("Hello, World!")
    .foregroundColor(.blue)
    .font(.title)
```

### View Protocol and Body

```swift
import SwiftUI

struct ContentView: View {
    var body: some View {
        Text("Hello, SwiftUI!")
            .font(.largeTitle)
            .foregroundColor(.primary)
    }
}

// Custom view with parameters
struct WelcomeView: View {
    let userName: String
    let isFirstTime: Bool
    
    var body: some View {
        VStack(spacing: 20) {
            Text("Welcome, \(userName)!")
                .font(.title)
                .fontWeight(.bold)
            
            if isFirstTime {
                Text("Thanks for joining us!")
                    .font(.subheadline)
                    .foregroundColor(.secondary)
            }
        }
        .padding()
    }
}
```

## 📱 Basic UI Components

### Text and Styling

```swift
struct TextExamples: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            // Basic text
            Text("Simple text")
            
            // Styled text
            Text("Styled Text")
                .font(.title2)
                .fontWeight(.semibold)
                .foregroundColor(.blue)
            
            // Multi-line text
            Text("This is a longer text that will wrap to multiple lines when the content is too wide for the screen.")
                .lineLimit(nil)
                .multilineTextAlignment(.leading)
            
            // Text with formatting
            Text("**Bold** and *italic* text")
                .font(.body)
            
            // Concatenated text with different styles
            Text("Price: ")
                .font(.body) +
            Text("$29.99")
                .font(.title2)
                .fontWeight(.bold)
                .foregroundColor(.green)
        }
        .padding()
    }
}
```

### Images and SF Symbols

```swift
struct ImageExamples: View {
    var body: some View {
        VStack(spacing: 20) {
            // SF Symbol
            Image(systemName: "heart.fill")
                .font(.largeTitle)
                .foregroundColor(.red)
            
            // Custom image
            Image("app-logo")
                .resizable()
                .aspectRatio(contentMode: .fit)
                .frame(width: 100, height: 100)
                .clipShape(Circle())
            
            // Async image loading (iOS 15+)
            AsyncImage(url: URL(string: "https://picsum.photos/200")) { image in
                image
                    .resizable()
                    .aspectRatio(contentMode: .fill)
            } placeholder: {
                ProgressView()
            }
            .frame(width: 200, height: 200)
            .clipShape(RoundedRectangle(cornerRadius: 12))
        }
    }
}
```

### Buttons and Actions

```swift
struct ButtonExamples: View {
    @State private var counter = 0
    @State private var isLiked = false
    
    var body: some View {
        VStack(spacing: 20) {
            // Basic button
            Button("Tap Me") {
                counter += 1
            }
            .buttonStyle(.borderedProminent)
            
            // Custom button with icon
            Button(action: {
                isLiked.toggle()
            }) {
                HStack {
                    Image(systemName: isLiked ? "heart.fill" : "heart")
                    Text(isLiked ? "Liked" : "Like")
                }
                .foregroundColor(isLiked ? .red : .primary)
            }
            .buttonStyle(.bordered)
            
            // Counter display
            Text("Counter: \(counter)")
                .font(.title2)
            
            // Destructive button
            Button("Reset", role: .destructive) {
                counter = 0
                isLiked = false
            }
        }
        .padding()
    }
}
```

## 📐 Layout System

### Stacks - The Foundation

```swift
struct StackExamples: View {
    var body: some View {
        VStack(spacing: 20) {
            // HStack - Horizontal arrangement
            HStack(spacing: 16) {
                Image(systemName: "person.circle.fill")
                    .font(.title)
                VStack(alignment: .leading) {
                    Text("John Doe")
                        .font(.headline)
                    Text("iOS Developer")
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                }
                Spacer()
                Button("Follow") { }
                    .buttonStyle(.bordered)
            }
            .padding()
            .background(Color(.systemGray6))
            .cornerRadius(12)
            
            // ZStack - Layered arrangement
            ZStack {
                RoundedRectangle(cornerRadius: 20)
                    .fill(LinearGradient(
                        colors: [.blue, .purple],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    ))
                    .frame(height: 150)
                
                VStack {
                    Text("Featured")
                        .font(.title2)
                        .fontWeight(.bold)
                        .foregroundColor(.white)
                    Text("Special Offer")
                        .font(.subheadline)
                        .foregroundColor(.white.opacity(0.8))
                }
            }
        }
        .padding()
    }
}
```

### LazyVStack and LazyHStack

```swift
struct LazyStackExample: View {
    let items = Array(1...1000)
    
    var body: some View {
        ScrollView {
            LazyVStack(spacing: 8) {
                ForEach(items, id: \.self) { item in
                    HStack {
                        Text("Item \(item)")
                        Spacer()
                        Text("Value")
                            .foregroundColor(.secondary)
                    }
                    .padding()
                    .background(Color(.systemGray6))
                    .cornerRadius(8)
                }
            }
            .padding()
        }
    }
}
```

### Grid Layouts

```swift
struct GridExample: View {
    let colors: [Color] = [.red, .blue, .green, .orange, .purple, .pink]
    
    let columns = [
        GridItem(.adaptive(minimum: 100))
    ]
    
    var body: some View {
        ScrollView {
            LazyVGrid(columns: columns, spacing: 16) {
                ForEach(colors.indices, id: \.self) { index in
                    RoundedRectangle(cornerRadius: 12)
                        .fill(colors[index])
                        .frame(height: 100)
                        .overlay(
                            Text("Item \(index + 1)")
                                .foregroundColor(.white)
                                .fontWeight(.semibold)
                        )
                }
            }
            .padding()
        }
    }
}
```

## 🔄 State Management

### @State - Local State

```swift
struct CounterView: View {
    @State private var count = 0
    @State private var isAnimating = false
    
    var body: some View {
        VStack(spacing: 30) {
            Text("\(count)")
                .font(.system(size: 60, weight: .bold, design: .rounded))
                .scaleEffect(isAnimating ? 1.2 : 1.0)
                .animation(.spring(response: 0.3), value: isAnimating)
            
            HStack(spacing: 20) {
                Button("-") {
                    count -= 1
                    animateChange()
                }
                .buttonStyle(.bordered)
                .disabled(count <= 0)
                
                Button("+") {
                    count += 1
                    animateChange()
                }
                .buttonStyle(.borderedProminent)
            }
            
            Button("Reset") {
                count = 0
                animateChange()
            }
            .buttonStyle(.bordered)
        }
        .padding()
    }
    
    private func animateChange() {
        isAnimating = true
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.1) {
            isAnimating = false
        }
    }
}
```

### @Binding - Shared State

```swift
struct SettingsView: View {
    @State private var isNotificationsEnabled = true
    @State private var isDarkModeEnabled = false
    @State private var fontSize: Double = 16
    
    var body: some View {
        NavigationView {
            Form {
                Section("Preferences") {
                    ToggleRow(
                        title: "Notifications",
                        isOn: $isNotificationsEnabled
                    )
                    
                    ToggleRow(
                        title: "Dark Mode",
                        isOn: $isDarkModeEnabled
                    )
                }
                
                Section("Appearance") {
                    SliderRow(
                        title: "Font Size",
                        value: $fontSize,
                        range: 12...24
                    )
                }
            }
            .navigationTitle("Settings")
        }
    }
}

struct ToggleRow: View {
    let title: String
    @Binding var isOn: Bool
    
    var body: some View {
        HStack {
            Text(title)
            Spacer()
            Toggle("", isOn: $isOn)
        }
    }
}

struct SliderRow: View {
    let title: String
    @Binding var value: Double
    let range: ClosedRange<Double>
    
    var body: some View {
        VStack(alignment: .leading) {
            HStack {
                Text(title)
                Spacer()
                Text("\(Int(value))")
                    .foregroundColor(.secondary)
            }
            Slider(value: $value, in: range, step: 1)
        }
    }
}
```

### @ObservableObject and @StateObject

```swift
import Combine

class UserStore: ObservableObject {
    @Published var users: [User] = []
    @Published var isLoading = false
    @Published var errorMessage: String?
    
    func loadUsers() {
        isLoading = true
        errorMessage = nil
        
        // Simulate network request
        DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
            self.users = [
                User(name: "Alice", email: "alice@example.com"),
                User(name: "Bob", email: "bob@example.com"),
                User(name: "Charlie", email: "charlie@example.com")
            ]
            self.isLoading = false
        }
    }
    
    func addUser(_ user: User) {
        users.append(user)
    }
    
    func deleteUser(at indexSet: IndexSet) {
        users.remove(atOffsets: indexSet)
    }
}

struct User: Identifiable {
    let id = UUID()
    let name: String
    let email: String
}

struct UserListView: View {
    @StateObject private var userStore = UserStore()
    @State private var showingAddUser = false
    
    var body: some View {
        NavigationView {
            Group {
                if userStore.isLoading {
                    ProgressView("Loading users...")
                } else if userStore.users.isEmpty {
                    ContentUnavailableView(
                        "No Users",
                        systemImage: "person.slash",
                        description: Text("Tap the + button to add users")
                    )
                } else {
                    List {
                        ForEach(userStore.users) { user in
                            UserRow(user: user)
                        }
                        .onDelete(perform: userStore.deleteUser)
                    }
                }
            }
            .navigationTitle("Users")
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Add") {
                        showingAddUser = true
                    }
                }
            }
            .sheet(isPresented: $showingAddUser) {
                AddUserView(userStore: userStore)
            }
            .onAppear {
                if userStore.users.isEmpty {
                    userStore.loadUsers()
                }
            }
        }
    }
}

struct UserRow: View {
    let user: User
    
    var body: some View {
        HStack {
            Circle()
                .fill(Color.blue)
                .frame(width: 40, height: 40)
                .overlay(
                    Text(String(user.name.prefix(1)))
                        .foregroundColor(.white)
                        .fontWeight(.semibold)
                )
            
            VStack(alignment: .leading) {
                Text(user.name)
                    .font(.headline)
                Text(user.email)
                    .font(.subheadline)
                    .foregroundColor(.secondary)
            }
            
            Spacer()
        }
        .padding(.vertical, 4)
    }
}

struct AddUserView: View {
    @ObservedObject var userStore: UserStore
    @Environment(\.dismiss) private var dismiss
    
    @State private var name = ""
    @State private var email = ""
    
    var body: some View {
        NavigationView {
            Form {
                Section("User Information") {
                    TextField("Name", text: $name)
                    TextField("Email", text: $email)
                        .keyboardType(.emailAddress)
                        .autocapitalization(.none)
                }
            }
            .navigationTitle("Add User")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("Cancel") {
                        dismiss()
                    }
                }
                
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Save") {
                        let newUser = User(name: name, email: email)
                        userStore.addUser(newUser)
                        dismiss()
                    }
                    .disabled(name.isEmpty || email.isEmpty)
                }
            }
        }
    }
}
```

## 🧭 Navigation

### NavigationView and NavigationLink

```swift
struct NavigationExample: View {
    let categories = ["Technology", "Science", "Sports", "Entertainment"]
    
    var body: some View {
        NavigationView {
            List(categories, id: \.self) { category in
                NavigationLink(destination: CategoryDetailView(category: category)) {
                    HStack {
                        Image(systemName: iconForCategory(category))
                            .foregroundColor(.blue)
                            .frame(width: 30)
                        Text(category)
                            .font(.headline)
                    }
                    .padding(.vertical, 4)
                }
            }
            .navigationTitle("Categories")
        }
    }
    
    private func iconForCategory(_ category: String) -> String {
        switch category {
        case "Technology": return "laptopcomputer"
        case "Science": return "atom"
        case "Sports": return "sportscourt"
        case "Entertainment": return "tv"
        default: return "folder"
        }
    }
}

struct CategoryDetailView: View {
    let category: String
    
    var body: some View {
        VStack(spacing: 20) {
            Image(systemName: "star.fill")
                .font(.system(size: 60))
                .foregroundColor(.yellow)
            
            Text("Welcome to \(category)")
                .font(.title)
                .fontWeight(.bold)
            
            Text("This is the detail view for the \(category) category.")
                .font(.body)
                .multilineTextAlignment(.center)
                .padding()
        }
        .navigationTitle(category)
        .navigationBarTitleDisplayMode(.large)
    }
}
```

### TabView

```swift
struct MainTabView: View {
    var body: some View {
        TabView {
            HomeView()
                .tabItem {
                    Image(systemName: "house")
                    Text("Home")
                }
            
            SearchView()
                .tabItem {
                    Image(systemName: "magnifyingglass")
                    Text("Search")
                }
            
            FavoritesView()
                .tabItem {
                    Image(systemName: "heart")
                    Text("Favorites")
                }
            
            ProfileView()
                .tabItem {
                    Image(systemName: "person")
                    Text("Profile")
                }
        }
    }
}

struct HomeView: View {
    var body: some View {
        NavigationView {
            Text("Home Content")
                .navigationTitle("Home")
        }
    }
}

struct SearchView: View {
    var body: some View {
        NavigationView {
            Text("Search Content")
                .navigationTitle("Search")
        }
    }
}

struct FavoritesView: View {
    var body: some View {
        NavigationView {
            Text("Favorites Content")
                .navigationTitle("Favorites")
        }
    }
}

struct ProfileView: View {
    var body: some View {
        NavigationView {
            Text("Profile Content")
                .navigationTitle("Profile")
        }
    }
}
```

## 🎨 Styling and Modifiers

### Custom Modifiers

```swift
struct CardModifier: ViewModifier {
    func body(content: Content) -> some View {
        content
            .padding()
            .background(Color(.systemBackground))
            .cornerRadius(12)
            .shadow(color: .black.opacity(0.1), radius: 5, x: 0, y: 2)
    }
}

extension View {
    func cardStyle() -> some View {
        modifier(CardModifier())
    }
}

// Usage
struct StyledView: View {
    var body: some View {
        VStack(spacing: 16) {
            Text("Card 1")
                .cardStyle()
            
            Text("Card 2")
                .cardStyle()
        }
        .padding()
    }
}
```

### Environment and Themes

```swift
struct ThemeKey: EnvironmentKey {
    static let defaultValue = Theme.light
}

extension EnvironmentValues {
    var theme: Theme {
        get { self[ThemeKey.self] }
        set { self[ThemeKey.self] = newValue }
    }
}

struct Theme {
    let backgroundColor: Color
    let textColor: Color
    let accentColor: Color
    
    static let light = Theme(
        backgroundColor: .white,
        textColor: .black,
        accentColor: .blue
    )
    
    static let dark = Theme(
        backgroundColor: .black,
        textColor: .white,
        accentColor: .orange
    )
}

struct ThemedView: View {
    @Environment(\.theme) var theme
    
    var body: some View {
        VStack {
            Text("Themed Content")
                .foregroundColor(theme.textColor)
            
            Button("Action") { }
                .foregroundColor(theme.accentColor)
        }
        .background(theme.backgroundColor)
    }
}
```

## 🎯 Real-World Project: Weather App

```swift
import SwiftUI

struct WeatherApp: View {
    @StateObject private var weatherStore = WeatherStore()
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 20) {
                    if let weather = weatherStore.currentWeather {
                        CurrentWeatherCard(weather: weather)
                        
                        HourlyForecastView(forecast: weatherStore.hourlyForecast)
                        
                        DailyForecastView(forecast: weatherStore.dailyForecast)
                    } else if weatherStore.isLoading {
                        ProgressView("Loading weather...")
                            .frame(maxWidth: .infinity, maxHeight: .infinity)
                    } else {
                        ContentUnavailableView(
                            "No Weather Data",
                            systemImage: "cloud.slash",
                            description: Text("Pull to refresh")
                        )
                    }
                }
                .padding()
            }
            .navigationTitle("Weather")
            .refreshable {
                await weatherStore.loadWeather()
            }
        }
        .task {
            await weatherStore.loadWeather()
        }
    }
}

struct CurrentWeatherCard: View {
    let weather: Weather
    
    var body: some View {
        VStack(spacing: 16) {
            HStack {
                VStack(alignment: .leading) {
                    Text(weather.location)
                        .font(.title2)
                        .fontWeight(.semibold)
                    
                    Text("Today")
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                }
                
                Spacer()
                
                VStack(alignment: .trailing) {
                    Text("\(weather.temperature)°")
                        .font(.system(size: 48, weight: .thin))
                    
                    Text(weather.condition)
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                }
            }
            
            HStack {
                WeatherDetail(title: "Feels like", value: "\(weather.feelsLike)°")
                Spacer()
                WeatherDetail(title: "Humidity", value: "\(weather.humidity)%")
                Spacer()
                WeatherDetail(title: "Wind", value: "\(weather.windSpeed) mph")
            }
        }
        .padding()
        .background(
            LinearGradient(
                colors: [.blue.opacity(0.6), .purple.opacity(0.6)],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
        )
        .foregroundColor(.white)
        .cornerRadius(16)
    }
}

struct WeatherDetail: View {
    let title: String
    let value: String
    
    var body: some View {
        VStack {
            Text(title)
                .font(.caption)
                .opacity(0.8)
            Text(value)
                .font(.subheadline)
                .fontWeight(.semibold)
        }
    }
}

struct HourlyForecastView: View {
    let forecast: [HourlyWeather]
    
    var body: some View {
        VStack(alignment: .leading) {
            Text("Hourly Forecast")
                .font(.headline)
                .padding(.horizontal)
            
            ScrollView(.horizontal, showsIndicators: false) {
                HStack(spacing: 16) {
                    ForEach(forecast) { hour in
                        VStack(spacing: 8) {
                            Text(hour.time)
                                .font(.caption)
                                .foregroundColor(.secondary)
                            
                            Image(systemName: hour.icon)
                                .font(.title2)
                                .foregroundColor(.blue)
                            
                            Text("\(hour.temperature)°")
                                .font(.subheadline)
                                .fontWeight(.semibold)
                        }
                        .padding(.vertical, 12)
                        .padding(.horizontal, 16)
                        .background(Color(.systemGray6))
                        .cornerRadius(12)
                    }
                }
                .padding(.horizontal)
            }
        }
    }
}

struct DailyForecastView: View {
    let forecast: [DailyWeather]
    
    var body: some View {
        VStack(alignment: .leading) {
            Text("7-Day Forecast")
                .font(.headline)
                .padding(.horizontal)
            
            VStack(spacing: 0) {
                ForEach(forecast) { day in
                    HStack {
                        Text(day.day)
                            .font(.subheadline)
                            .frame(width: 60, alignment: .leading)
                        
                        Image(systemName: day.icon)
                            .font(.title3)
                            .foregroundColor(.blue)
                            .frame(width: 30)
                        
                        Spacer()
                        
                        Text("\(day.low)°")
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                        
                        Text("\(day.high)°")
                            .font(.subheadline)
                            .fontWeight(.semibold)
                            .frame(width: 40, alignment: .trailing)
                    }
                    .padding(.horizontal)
                    .padding(.vertical, 12)
                    
                    if day.id != forecast.last?.id {
                        Divider()
                            .padding(.horizontal)
                    }
                }
            }
            .background(Color(.systemGray6))
            .cornerRadius(12)
            .padding(.horizontal)
        }
    }
}

// Data Models
struct Weather {
    let location: String
    let temperature: Int
    let condition: String
    let feelsLike: Int
    let humidity: Int
    let windSpeed: Int
}

struct HourlyWeather: Identifiable {
    let id = UUID()
    let time: String
    let temperature: Int
    let icon: String
}

struct DailyWeather: Identifiable {
    let id = UUID()
    let day: String
    let high: Int
    let low: Int
    let icon: String
}

// Store
class WeatherStore: ObservableObject {
    @Published var currentWeather: Weather?
    @Published var hourlyForecast: [HourlyWeather] = []
    @Published var dailyForecast: [DailyWeather] = []
    @Published var isLoading = false
    
    func loadWeather() async {
        await MainActor.run {
            isLoading = true
        }
        
        // Simulate API call
        try? await Task.sleep(nanoseconds: 1_000_000_000)
        
        await MainActor.run {
            currentWeather = Weather(
                location: "San Francisco",
                temperature: 72,
                condition: "Partly Cloudy",
                feelsLike: 75,
                humidity: 65,
                windSpeed: 8
            )
            
            hourlyForecast = [
                HourlyWeather(time: "Now", temperature: 72, icon: "cloud.sun"),
                HourlyWeather(time: "1 PM", temperature: 74, icon: "sun.max"),
                HourlyWeather(time: "2 PM", temperature: 76, icon: "sun.max"),
                HourlyWeather(time: "3 PM", temperature: 75, icon: "cloud.sun"),
                HourlyWeather(time: "4 PM", temperature: 73, icon: "cloud")
            ]
            
            dailyForecast = [
                DailyWeather(day: "Today", high: 76, low: 62, icon: "cloud.sun"),
                DailyWeather(day: "Tue", high: 78, low: 64, icon: "sun.max"),
                DailyWeather(day: "Wed", high: 75, low: 61, icon: "cloud.rain"),
                DailyWeather(day: "Thu", high: 73, low: 59, icon: "cloud.rain"),
                DailyWeather(day: "Fri", high: 71, low: 58, icon: "cloud"),
                DailyWeather(day: "Sat", high: 74, low: 60, icon: "sun.max"),
                DailyWeather(day: "Sun", high: 77, low: 63, icon: "sun.max")
            ]
            
            isLoading = false
        }
    }
}
```

## 📚 Key Takeaways

1. **Think Declaratively** - Describe what the UI should look like, not how to build it
2. **Use @State for Local Data** - Keep component state private when possible
3. **Leverage @Binding for Shared State** - Pass data between parent and child views
4. **Embrace Single Source of Truth** - Use @ObservableObject for shared app state
5. **Compose Views** - Break complex UIs into smaller, reusable components
6. **Use Environment for Themes** - Share configuration across the app hierarchy

## 🔗 What's Next?

In the next chapter, we'll explore **Navigation & User Input**, covering advanced navigation patterns, form handling, and user interaction techniques.

---

*Practice building these examples in Xcode to master SwiftUI fundamentals!*
