# Launch Time Optimization

> Achieve sub-second app launch times with proven optimization techniques

## 🎯 Learning Objectives

Master app launch optimization to create lightning-fast user experiences:
- Understand the app launch process and measurement techniques
- Implement cold and warm launch optimizations
- Optimize binary size and loading performance
- Use Xcode tools for performance profiling
- Apply real-world optimization strategies

## ⏱️ Understanding App Launch

### Launch Types and Phases

```swift
// App launch phases (measured by Xcode Organizer)
/*
1. Pre-main (System work before main() is called)
   - Dynamic library loading
   - Objective-C runtime setup
   - Static initializers
   - +load methods

2. Main (Your code execution)
   - main() function
   - UIApplicationMain
   - App delegate methods
   - First frame render

3. Post-main (First interaction)
   - View controller loading
   - Initial data loading
   - UI setup completion
*/

import UIKit

@main
class AppDelegate: UIResponder, UIApplicationDelegate {
    
    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        
        // 🚀 CRITICAL: Keep this method under 400ms
        let startTime = CFAbsoluteTimeGetCurrent()
        
        // Essential initialization only
        setupCrashReporting()
        setupAnalytics()
        
        // Defer heavy work
        DispatchQueue.main.async {
            self.performDeferredSetup()
        }
        
        let endTime = CFAbsoluteTimeGetCurrent()
        print("didFinishLaunching took: \((endTime - startTime) * 1000)ms")
        
        return true
    }
    
    private func setupCrashReporting() {
        // Lightweight crash reporting setup
        // FirebaseCrashlytics.crashlytics().setCrashlyticsCollectionEnabled(true)
    }
    
    private func setupAnalytics() {
        // Minimal analytics initialization
        // Analytics.configure()
    }
    
    private func performDeferredSetup() {
        // Heavy initialization after launch
        setupNetworking()
        preloadCriticalData()
        setupLocationServices()
    }
}
```

### Measuring Launch Performance

```swift
import os.signpost

class LaunchProfiler {
    private static let subsystem = "com.yourapp.performance"
    private static let category = "Launch"
    private static let log = OSLog(subsystem: subsystem, category: category)
    
    static func beginLaunchMeasurement() {
        os_signpost(.begin, log: log, name: "AppLaunch")
    }
    
    static func endLaunchMeasurement() {
        os_signpost(.end, log: log, name: "AppLaunch")
    }
    
    static func measureCriticalPath<T>(_ name: String, operation: () throws -> T) rethrows -> T {
        let signpostID = OSSignpostID(log: log)
        os_signpost(.begin, log: log, name: "CriticalPath", signpostID: signpostID, "%{public}s", name)
        
        let result = try operation()
        
        os_signpost(.end, log: log, name: "CriticalPath", signpostID: signpostID)
        return result
    }
}

// Usage in SceneDelegate
class SceneDelegate: UIResponder, UIWindowSceneDelegate {
    
    func scene(_ scene: UIScene, willConnectTo session: UISceneSession, options connectionOptions: UIScene.ConnectionOptions) {
        
        LaunchProfiler.beginLaunchMeasurement()
        
        guard let windowScene = (scene as? UIWindowScene) else { return }
        
        let window = UIWindow(windowScene: windowScene)
        
        // Measure critical UI setup
        let rootViewController = LaunchProfiler.measureCriticalPath("RootViewController") {
            return createRootViewController()
        }
        
        window.rootViewController = rootViewController
        window.makeKeyAndVisible()
        self.window = window
        
        // End measurement when first frame is ready
        DispatchQueue.main.async {
            LaunchProfiler.endLaunchMeasurement()
        }
    }
    
    private func createRootViewController() -> UIViewController {
        // Lightweight root view controller
        return MainTabBarController()
    }
}
```

## 🚀 Pre-Main Optimizations

### Reducing Dynamic Library Loading

```swift
// ❌ Avoid importing unnecessary frameworks
import UIKit
import Foundation
// import SomeHeavyFramework  // Only import if actually used

// ✅ Use @_implementationOnly for internal dependencies
@_implementationOnly import InternalUtilities

// ✅ Lazy framework loading
class FrameworkManager {
    private var heavyFramework: AnyObject?
    
    func getHeavyFramework() -> AnyObject? {
        if heavyFramework == nil {
            // Load framework only when needed
            heavyFramework = loadHeavyFrameworkDynamically()
        }
        return heavyFramework
    }
    
    private func loadHeavyFrameworkDynamically() -> AnyObject? {
        // Dynamic loading implementation
        return nil
    }
}
```

### Optimizing Static Initializers

```swift
// ❌ Heavy work in static initializers
class BadExample {
    static let expensiveResource = createExpensiveResource() // Runs at launch!
    
    static func createExpensiveResource() -> SomeResource {
        // This runs during pre-main phase
        return SomeResource()
    }
}

// ✅ Lazy initialization
class GoodExample {
    private static var _expensiveResource: SomeResource?
    
    static var expensiveResource: SomeResource {
        if _expensiveResource == nil {
            _expensiveResource = createExpensiveResource()
        }
        return _expensiveResource!
    }
    
    private static func createExpensiveResource() -> SomeResource {
        return SomeResource()
    }
}

// ✅ Even better: Use lazy property
class BestExample {
    static let expensiveResource: SomeResource = {
        return SomeResource()
    }()
}
```

### Eliminating +load Methods

```swift
// ❌ Avoid +load methods (they block launch)
extension UIViewController {
    @objc static func load() {
        // This runs during pre-main and blocks launch
        setupSwizzling()
    }
}

// ✅ Use +initialize or lazy setup instead
extension UIViewController {
    @objc static func initialize() {
        // Runs when class is first used
        if self == UIViewController.self {
            setupSwizzling()
        }
    }
}

// ✅ Or defer setup until needed
class ViewControllerSetup {
    private static var isSetup = false
    
    static func ensureSetup() {
        guard !isSetup else { return }
        setupSwizzling()
        isSetup = true
    }
}
```

## 📱 Main Phase Optimizations

### Optimizing App Delegate

```swift
@main
class OptimizedAppDelegate: UIResponder, UIApplicationDelegate {
    
    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        
        // ✅ Only essential, synchronous setup
        setupCrashReporting()
        
        // ✅ Defer everything else
        deferHeavySetup()
        
        return true
    }
    
    private func deferHeavySetup() {
        // Use different queues based on priority
        
        // High priority - needed soon
        DispatchQueue.main.async {
            self.setupAnalytics()
            self.setupPushNotifications()
        }
        
        // Medium priority - can wait a bit
        DispatchQueue.global(qos: .userInitiated).async {
            self.setupNetworking()
            self.preloadCriticalData()
        }
        
        // Low priority - background setup
        DispatchQueue.global(qos: .utility).async {
            self.setupLocationServices()
            self.cleanupOldFiles()
        }
    }
    
    private func setupCrashReporting() {
        // Minimal crash reporting - must be synchronous
    }
    
    private func setupAnalytics() {
        // Analytics can be async
    }
    
    private func setupPushNotifications() {
        UNUserNotificationCenter.current().requestAuthorization(options: [.alert, .badge, .sound]) { _, _ in }
    }
    
    private func setupNetworking() {
        // Configure URLSession, etc.
    }
    
    private func preloadCriticalData() {
        // Load data that will be needed immediately
    }
    
    private func setupLocationServices() {
        // Heavy location setup
    }
    
    private func cleanupOldFiles() {
        // File cleanup can happen in background
    }
}
```

### Optimizing Root View Controller

```swift
class FastRootViewController: UIViewController {
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // ✅ Minimal UI setup only
        setupBasicUI()
        
        // ✅ Defer heavy operations
        DispatchQueue.main.async {
            self.setupComplexUI()
        }
        
        // ✅ Load data asynchronously
        loadInitialData()
    }
    
    private func setupBasicUI() {
        // Only essential UI elements
        view.backgroundColor = .systemBackground
        
        // Show loading state immediately
        showLoadingState()
    }
    
    private func setupComplexUI() {
        // Complex UI setup after first frame
        setupNavigationBar()
        setupTabBar()
        setupGestures()
    }
    
    private func showLoadingState() {
        let loadingView = UIActivityIndicatorView(style: .large)
        loadingView.startAnimating()
        loadingView.center = view.center
        view.addSubview(loadingView)
    }
    
    private func loadInitialData() {
        Task {
            do {
                let data = try await DataManager.shared.loadCriticalData()
                await MainActor.run {
                    self.updateUI(with: data)
                }
            } catch {
                await MainActor.run {
                    self.showError(error)
                }
            }
        }
    }
}
```

## 🗂️ Binary Size Optimization

### Asset Optimization

```swift
// ✅ Use asset catalogs for automatic optimization
// Assets.xcassets automatically provides:
// - Image compression
// - Device-specific variants
// - App thinning support

class ImageManager {
    // ✅ Lazy image loading
    private static var imageCache: [String: UIImage] = [:]
    
    static func image(named name: String) -> UIImage? {
        if let cached = imageCache[name] {
            return cached
        }
        
        let image = UIImage(named: name)
        imageCache[name] = image
        return image
    }
    
    // ✅ Async image loading for large images
    static func loadLargeImage(named name: String) async -> UIImage? {
        return await withCheckedContinuation { continuation in
            DispatchQueue.global(qos: .userInitiated).async {
                let image = UIImage(named: name)
                continuation.resume(returning: image)
            }
        }
    }
}

// ✅ Use SF Symbols when possible (zero binary size impact)
extension UIImage {
    static func systemIcon(_ name: String, size: CGFloat = 24) -> UIImage? {
        let config = UIImage.SymbolConfiguration(pointSize: size)
        return UIImage(systemName: name, withConfiguration: config)
    }
}
```

### Code Size Optimization

```swift
// ✅ Use generics to reduce code duplication
protocol Cacheable {
    associatedtype Key: Hashable
    var cacheKey: Key { get }
}

class GenericCache<T: Cacheable> {
    private var cache: [T.Key: T] = [:]
    
    func store(_ item: T) {
        cache[item.cacheKey] = item
    }
    
    func retrieve(key: T.Key) -> T? {
        return cache[key]
    }
}

// ✅ Use protocol extensions for shared behavior
protocol ViewConfigurable {
    func configure()
}

extension ViewConfigurable where Self: UIView {
    func applyCommonStyling() {
        layer.cornerRadius = 8
        layer.shadowOpacity = 0.1
        layer.shadowRadius = 4
    }
}

// ✅ Avoid large switch statements - use lookup tables
class IconProvider {
    private static let iconMap: [String: String] = [
        "home": "house",
        "profile": "person.circle",
        "settings": "gear",
        "search": "magnifyingglass"
    ]
    
    static func icon(for type: String) -> String {
        return iconMap[type] ?? "questionmark"
    }
}
```

## 📊 Performance Monitoring

### Real-Time Launch Metrics

```swift
import MetricKit

class LaunchMetrics: NSObject, MXMetricManagerSubscriber {
    static let shared = LaunchMetrics()
    
    override init() {
        super.init()
        MXMetricManager.shared.add(self)
    }
    
    func didReceive(_ payloads: [MXMetricPayload]) {
        for payload in payloads {
            if let launchMetrics = payload.applicationLaunchMetrics {
                processlLaunchMetrics(launchMetrics)
            }
        }
    }
    
    private func processlLaunchMetrics(_ metrics: MXApplicationLaunchMetrics) {
        // Track launch time trends
        let timeToFirstDraw = metrics.histogrammedTimeToFirstDraw
        let resumeTime = metrics.histogrammedApplicationResumeTime
        
        // Send to analytics
        Analytics.track("app_launch_performance", parameters: [
            "time_to_first_draw": timeToFirstDraw.averageValue,
            "resume_time": resumeTime?.averageValue ?? 0
        ])
        
        // Alert if performance degrades
        if timeToFirstDraw.averageValue > 2.0 { // 2 seconds
            reportPerformanceIssue("Slow launch detected")
        }
    }
    
    private func reportPerformanceIssue(_ message: String) {
        // Report to crash reporting service
        print("Performance Issue: \(message)")
    }
}
```

### Custom Launch Timing

```swift
class LaunchTimer {
    private static var startTime: CFAbsoluteTime = 0
    private static var milestones: [String: CFAbsoluteTime] = [:]
    
    static func start() {
        startTime = CFAbsoluteTimeGetCurrent()
    }
    
    static func milestone(_ name: String) {
        let currentTime = CFAbsoluteTimeGetCurrent()
        milestones[name] = currentTime - startTime
        
        print("Launch milestone '\(name)': \((currentTime - startTime) * 1000)ms")
    }
    
    static func complete() {
        let totalTime = CFAbsoluteTimeGetCurrent() - startTime
        print("Total launch time: \((totalTime) * 1000)ms")
        
        // Send metrics to analytics
        Analytics.track("app_launch_complete", parameters: [
            "total_time": totalTime,
            "milestones": milestones
        ])
    }
}

// Usage throughout app launch
@main
class AppDelegate: UIResponder, UIApplicationDelegate {
    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        
        LaunchTimer.start()
        LaunchTimer.milestone("app_delegate_start")
        
        // Setup code...
        
        LaunchTimer.milestone("app_delegate_complete")
        return true
    }
}
```

## 🛠️ Xcode Optimization Tools

### Using Instruments for Launch Analysis

```swift
// Add this to measure specific code paths
import os.signpost

class InstrumentsProfiler {
    private static let log = OSLog(subsystem: "com.yourapp.performance", category: "Launch")
    
    static func measureBlock<T>(_ name: String, block: () throws -> T) rethrows -> T {
        os_signpost(.begin, log: log, name: "LaunchBlock", "%{public}s", name)
        let result = try block()
        os_signpost(.end, log: log, name: "LaunchBlock")
        return result
    }
    
    static func measureAsync<T>(_ name: String, block: () async throws -> T) async rethrows -> T {
        os_signpost(.begin, log: log, name: "AsyncLaunchBlock", "%{public}s", name)
        let result = try await block()
        os_signpost(.end, log: log, name: "AsyncLaunchBlock")
        return result
    }
}

// Usage
class DataLoader {
    func loadCriticalData() async throws -> [DataModel] {
        return try await InstrumentsProfiler.measureAsync("LoadCriticalData") {
            // Your data loading code
            return try await performNetworkRequest()
        }
    }
}
```

### Build Settings for Launch Optimization

```swift
/*
Recommended Xcode build settings for launch optimization:

1. Optimization Level: 
   - Debug: -Onone (for debugging)
   - Release: -O (for performance)

2. Link-Time Optimization: YES
   - Enables cross-module optimizations

3. Strip Debug Symbols: YES (Release only)
   - Reduces binary size

4. Dead Code Stripping: YES
   - Removes unused code

5. Asset Catalog Compiler Options:
   - Optimization: space
   - Output Format: automatic

6. Swift Compilation Mode:
   - Debug: Incremental
   - Release: Whole Module

Build Settings in code (for reference):
*/

// You can check these at runtime
#if DEBUG
let isOptimized = false
#else
let isOptimized = true
#endif
```

## 🎯 Real-World Launch Optimization

### Complete Optimized App Structure

```swift
import UIKit
import os.signpost

@main
class OptimizedAppDelegate: UIResponder, UIApplicationDelegate {
    
    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        
        // Start performance monitoring
        LaunchProfiler.beginLaunchMeasurement()
        
        // Only critical setup
        setupCrashReporting()
        
        // Defer everything else
        scheduleBackgroundSetup()
        
        LaunchProfiler.milestone("app_delegate_complete")
        return true
    }
    
    private func setupCrashReporting() {
        // Minimal crash reporting setup
        // Must be synchronous and fast
    }
    
    private func scheduleBackgroundSetup() {
        // Prioritized background setup
        DispatchQueue.main.async { [weak self] in
            self?.setupHighPriorityServices()
        }
        
        DispatchQueue.global(qos: .userInitiated).async { [weak self] in
            self?.setupMediumPriorityServices()
        }
        
        DispatchQueue.global(qos: .utility).async { [weak self] in
            self?.setupLowPriorityServices()
        }
    }
    
    private func setupHighPriorityServices() {
        LaunchProfiler.measureCriticalPath("HighPrioritySetup") {
            // Analytics, push notifications
            Analytics.configure()
            NotificationManager.setup()
        }
    }
    
    private func setupMediumPriorityServices() {
        LaunchProfiler.measureCriticalPath("MediumPrioritySetup") {
            // Networking, data preloading
            NetworkManager.configure()
            DataCache.preloadCriticalData()
        }
    }
    
    private func setupLowPriorityServices() {
        LaunchProfiler.measureCriticalPath("LowPrioritySetup") {
            // Location, file cleanup, etc.
            LocationManager.setup()
            FileManager.cleanupOldFiles()
        }
    }
}

class OptimizedSceneDelegate: UIResponder, UIWindowSceneDelegate {
    var window: UIWindow?
    
    func scene(_ scene: UIScene, willConnectTo session: UISceneSession, options connectionOptions: UIScene.ConnectionOptions) {
        
        guard let windowScene = (scene as? UIWindowScene) else { return }
        
        // Fast UI setup
        let window = UIWindow(windowScene: windowScene)
        
        // Lightweight root controller
        let rootController = LaunchProfiler.measureCriticalPath("CreateRootController") {
            return createOptimizedRootController()
        }
        
        window.rootViewController = rootController
        window.makeKeyAndVisible()
        self.window = window
        
        // Complete launch measurement
        DispatchQueue.main.async {
            LaunchProfiler.endLaunchMeasurement()
        }
    }
    
    private func createOptimizedRootController() -> UIViewController {
        // Return lightweight controller that shows loading state
        return LaunchViewController()
    }
}

class LaunchViewController: UIViewController {
    private let loadingView = UIActivityIndicatorView(style: .large)
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // Minimal UI setup
        setupLoadingUI()
        
        // Load main interface asynchronously
        loadMainInterface()
    }
    
    private func setupLoadingUI() {
        view.backgroundColor = .systemBackground
        
        loadingView.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(loadingView)
        
        NSLayoutConstraint.activate([
            loadingView.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            loadingView.centerYAnchor.constraint(equalTo: view.centerYAnchor)
        ])
        
        loadingView.startAnimating()
    }
    
    private func loadMainInterface() {
        Task {
            // Load critical data
            await DataManager.shared.loadInitialData()
            
            // Switch to main interface
            await MainActor.run {
                let mainController = MainTabBarController()
                
                // Smooth transition
                UIView.transition(with: view.window!, duration: 0.3, options: .transitionCrossDissolve) {
                    self.view.window?.rootViewController = mainController
                }
            }
        }
    }
}
```

## 📈 Performance Targets

### Industry Benchmarks

```swift
struct LaunchPerformanceTargets {
    // Apple's recommendations
    static let coldLaunchTarget: TimeInterval = 0.4  // 400ms
    static let warmLaunchTarget: TimeInterval = 0.2  // 200ms
    
    // Real-world targets
    static let goodColdLaunch: TimeInterval = 1.0    // 1 second
    static let acceptableColdLaunch: TimeInterval = 2.0  // 2 seconds
    
    // Binary size targets
    static let maxBinarySize: Int = 100 * 1024 * 1024  // 100MB
    static let idealBinarySize: Int = 50 * 1024 * 1024   // 50MB
}

class PerformanceValidator {
    static func validateLaunchTime(_ time: TimeInterval) -> LaunchPerformance {
        switch time {
        case 0..<LaunchPerformanceTargets.coldLaunchTarget:
            return .excellent
        case LaunchPerformanceTargets.coldLaunchTarget..<LaunchPerformanceTargets.goodColdLaunch:
            return .good
        case LaunchPerformanceTargets.goodColdLaunch..<LaunchPerformanceTargets.acceptableColdLaunch:
            return .acceptable
        default:
            return .poor
        }
    }
}

enum LaunchPerformance {
    case excellent, good, acceptable, poor
    
    var description: String {
        switch self {
        case .excellent: return "Excellent (< 400ms)"
        case .good: return "Good (< 1s)"
        case .acceptable: return "Acceptable (< 2s)"
        case .poor: return "Poor (> 2s)"
        }
    }
}
```

## 📚 Key Takeaways

1. **Measure First** - Use Instruments and MetricKit to identify bottlenecks
2. **Defer Heavy Work** - Only essential setup in main thread during launch
3. **Optimize Pre-Main** - Reduce dynamic libraries and static initializers
4. **Lazy Loading** - Load resources only when needed
5. **Binary Size Matters** - Smaller binaries launch faster
6. **Monitor Continuously** - Track launch performance over time
7. **Test on Real Devices** - Simulators don't reflect real performance

## 🔗 What's Next?

In the next chapter, we'll explore **Memory Management** techniques to keep your app running smoothly and avoid crashes due to memory pressure.

---

*Use Xcode's Instruments to profile your app's launch performance and apply these optimizations systematically!*
