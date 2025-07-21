# Basic Usage Examples

## 📚 Introduction

This guide provides simple, practical examples of using SuperClaude Pro commands in your daily workflow.

## 🔧 Basic Commands

### 1. Code Analysis

**Analyze a single file:**
```
/sc:analyze utils.py
```

**Analyze entire project:**
```
/sc:analyze
```

**With specific metrics:**
```
/sc:analyze --complexity --duplication --suggestions
```

### 2. Implementation

**Simple feature:**
```
/sc:implement "Add logging to the application"
```

**With specifications:**
```
/sc:implement "Create a user registration endpoint that:
- Validates email format
- Checks for existing users
- Sends confirmation email
- Returns appropriate status codes"
```

### 3. Testing

**Generate tests for a module:**
```
/sc:test models.py
```

**Create comprehensive test suite:**
```
/sc:test --comprehensive --fixtures --mocks
```

### 4. Documentation

**Document a function:**
```
/sc:document calculate_price
```

**Generate project documentation:**
```
/sc:document --readme --api-docs --examples
```

## 🤖 Working with Personas

### Architecture Design
```
"I need to design a microservices architecture for an e-commerce platform"
```
The **Architect** persona will activate and help with:
- System design
- Component interaction
- Technology choices
- Scalability considerations

### Security Review
```
"Review this authentication code for security vulnerabilities"
```
The **Security** persona will:
- Identify vulnerabilities
- Suggest fixes
- Recommend best practices
- Check for common exploits

### Frontend Development
```
"Create a responsive navigation component with dropdown menus"
```
The **Frontend** persona will:
- Use modern CSS/JS
- Ensure accessibility
- Optimize performance
- Follow best practices

## 🌊 Wave Orchestration Examples

### Complex Implementation
```
/sc:build "Complete user management system with:
- Registration and login
- Password reset
- Profile management
- Admin dashboard
- API documentation"
```

Wave will automatically:
1. Design the architecture
2. Implement components
3. Create tests
4. Generate documentation
5. Set up deployment configs

### Large-scale Refactoring
```
/sc:improve --refactor "Migrate from callbacks to async/await"
```

Wave handles:
1. Analyzing current code
2. Planning migration
3. Refactoring systematically
4. Updating tests
5. Verifying functionality

## 🔌 MCP Integration Examples

### Using Context7 for Documentation
```
/sc:implement "Create a data visualization dashboard using D3.js"
```
Context7 automatically provides:
- D3.js API documentation
- Best practices
- Example code
- Performance tips

### Browser Automation with Playwright
```
/sc:test --e2e "Test the checkout flow"
```
Playwright integration:
- Launches browser
- Simulates user actions
- Validates UI states
- Captures screenshots

## 💡 Practical Workflows

### Morning Code Review
```bash
# 1. Check code quality
/sc:analyze --since yesterday

# 2. Review security
"Check for any security issues in recent commits"

# 3. Update documentation
/sc:document --updated-only
```

### Feature Development
```bash
# 1. Design first
"Design a caching system for our API"

# 2. Implement
/sc:implement "Caching layer using Redis"

# 3. Test
/sc:test cache_manager.py

# 4. Document
/sc:document cache_manager.py --examples
```

### Bug Fixing
```bash
# 1. Analyze the issue
/sc:troubleshoot "Users report slow page load"

# 2. Find root cause
/sc:analyze --performance --bottlenecks

# 3. Fix
/sc:improve --optimize "Improve page load time"

# 4. Verify
/sc:test --performance
```

## 🎯 Pro Tips

### 1. Combine Commands
```
/sc:implement "Add feature X" && /sc:test && /sc:document
```

### 2. Use Specific Flags
```
/sc:analyze --focus security,performance
/sc:test --only integration
/sc:build --no-install
```

### 3. Leverage Context
```
# First, set context
"Working on the payment module"

# Then use commands - they'll focus on payment code
/sc:analyze
/sc:test
/sc:improve
```

### 4. Quick Iterations
```
# Make changes
/sc:implement "Add input validation"

# Test immediately
/sc:test --last-changes

# Fix issues
/sc:troubleshoot
```

## 📊 Common Patterns

### API Development
```bash
/sc:design "REST API for products"
/sc:implement
/sc:test --api
/sc:document --openapi
```

### Database Work
```bash
"Design database schema for blog"
/sc:implement "Create migrations"
/sc:test --database
```

### UI Components
```bash
/sc:implement "Reusable button component"
/sc:test --component
/sc:document --storybook
```

## Next Steps

- 🚀 Explore [Advanced Workflows](advanced-workflows.md)
- 🔧 Learn about [Custom Commands](custom-commands.md)
- 🔌 Check out [Integration Examples](integrations.md)

---

**Remember:** SuperClaude Pro adapts to your workflow. The more you use it, the better it understands your preferences!