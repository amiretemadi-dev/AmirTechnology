// Global variables
let isLiked = false
let likeCount = 42

// Initialize all features when DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  initializeAnimations()
  initializeFormHandlers()
  initializeDashboard()
  initializeNavigation()
  initializeComments()
  initializeLazyLoading()
  initializeSearch()
  initializeThemeSwitcher()
  initializeCopyButton() // Added copy button initialization
})

// Initialize animations
function initializeAnimations() {
  // Animate elements on scroll
  const observerOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -50px 0px",
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = "1"
        entry.target.style.transform = "translateY(0)"
      }
    })
  }, observerOptions)

  // Observe elements for animation
  const animateElements = document.querySelectorAll(".post-card, .contact-info-item, .stat-item")
  animateElements.forEach((el) => {
    el.style.opacity = "0"
    el.style.transform = "translateY(30px)"
    el.style.transition = "opacity 0.6s ease, transform 0.6s ease"
    observer.observe(el)
  })

  // Hero section animation
  const heroContent = document.querySelector(".hero-content")
  if (heroContent) {
    setTimeout(() => {
      heroContent.style.opacity = "1"
      heroContent.style.transform = "translateY(0)"
    }, 300)
  }
}

// Initialize form handlers
function initializeFormHandlers() {
  // Login form
  const loginForm = document.getElementById("loginForm")
  if (loginForm) {
    loginForm.addEventListener("submit", handleLoginForm)
  }

  // Register form
  const registerForm = document.getElementById("registerForm")
  if (registerForm) {
    registerForm.addEventListener("submit", handleRegisterForm)

    // Password confirmation validation
    const password = document.getElementById("password")
    const confirmPassword = document.getElementById("confirmPassword")
    const passwordMismatch = document.getElementById("passwordMismatch")

    if (confirmPassword) {
      confirmPassword.addEventListener("input", () => {
        if (password.value !== confirmPassword.value) {
          confirmPassword.classList.add("is-invalid")
          passwordMismatch.style.display = "block"
        } else {
          confirmPassword.classList.remove("is-invalid")
          passwordMismatch.style.display = "none"
        }
      })
    }
  }

  // Verification form
  const verifyForm = document.getElementById("verifyForm")
  if (verifyForm) {
    verifyForm.addEventListener("submit", handleVerifyForm)

    // Auto-format verification code
    const verificationCode = document.getElementById("verificationCode")
    if (verificationCode) {
      verificationCode.addEventListener("input", (e) => {
        let value = e.target.value.replace(/\D/g, "")
        if (value.length > 6) value = value.slice(0, 6)
        e.target.value = value
      })
    }
  }

  // Resend code
  const resendCode = document.getElementById("resendCode")
  if (resendCode) {
    resendCode.addEventListener("click", (e) => {
      e.preventDefault()
      showSuccessMessage("Verification code resent successfully!")
    })
  }

  // Profile image upload preview
  const profileForm = document.getElementById("profileForm")
  if (profileForm) {
    const profileImageUpload = document.getElementById("profileImageUpload")
    const currentProfileImage = document.getElementById("currentProfileImage")

    if (profileImageUpload && currentProfileImage) {
      profileImageUpload.addEventListener("change", (e) => {
        const file = e.target.files[0]
        if (file) {
          const reader = new FileReader()
          reader.onload = (e) => {
            currentProfileImage.src = e.target.result
          }
          reader.readAsDataURL(file)
        }
      })
    }
  }

  // Settings form
  const settingsForm = document.getElementById("settingsForm")
  if (settingsForm) {
    settingsForm.addEventListener("submit", handleSettingsForm)
  }
}

function handleLoginForm(e) {
  e.preventDefault()

  const form = e.target
  const submitBtn = form.querySelector('button[type="submit"]')
  const originalText = submitBtn.innerHTML

  submitBtn.innerHTML = '<span class="loading"></span> Signing In...'
  submitBtn.disabled = true

  setTimeout(() => {
    window.location.href = "verify.html"
  }, 1500)
}

function handleRegisterForm(e) {
  e.preventDefault()

  const form = e.target
  const password = document.getElementById("password").value
  const confirmPassword = document.getElementById("confirmPassword").value

  if (password !== confirmPassword) {
    showErrorMessage("Passwords do not match!")
    return
  }

  const submitBtn = form.querySelector('button[type="submit"]')
  const originalText = submitBtn.innerHTML

  submitBtn.innerHTML = '<span class="loading"></span> Creating Account...'
  submitBtn.disabled = true

  setTimeout(() => {
    window.location.href = "verify.html"
  }, 2000)
}

function handleVerifyForm(e) {
  e.preventDefault()

  const form = e.target
  const code = document.getElementById("verificationCode").value

  if (code.length !== 6) {
    showErrorMessage("Please enter a valid 6-digit code!")
    return
  }

  const submitBtn = form.querySelector('button[type="submit"]')
  const originalText = submitBtn.innerHTML

  submitBtn.innerHTML = '<span class="loading"></span> Verifying...'
  submitBtn.disabled = true

  setTimeout(() => {
    showSuccessMessage("Verification successful! Welcome to Amir-Tec!")
    setTimeout(() => {
      window.location.href = "index.html"
    }, 2000)
  }, 1500)
}

function handleSettingsForm(e) {
  e.preventDefault()

  const form = e.target
  const submitBtn = form.querySelector('button[type="submit"]')
  const originalText = submitBtn.innerHTML

  submitBtn.innerHTML = '<span class="loading"></span> Saving...'
  submitBtn.disabled = true

  setTimeout(() => {
    submitBtn.innerHTML = originalText
    submitBtn.disabled = false
    showSuccessMessage("Settings saved successfully!")
  }, 1500)
}

// Initialize dashboard
function initializeDashboard() {
  const dashboardNav = document.querySelectorAll(".dashboard-nav .nav-link")
  const dashboardSections = document.querySelectorAll(".dashboard-section")

  dashboardNav.forEach((link) => {
    link.addEventListener("click", function (e) {
      e.preventDefault()

      const targetSection = this.getAttribute("data-section")

      // Remove active class from all nav links and sections
      dashboardNav.forEach((nav) => nav.classList.remove("active"))
      dashboardSections.forEach((section) => section.classList.remove("active"))

      // Add active class to clicked nav and corresponding section
      this.classList.add("active")
      const targetElement = document.getElementById(targetSection + "-section")
      if (targetElement) {
        targetElement.classList.add("active")
      }
    })
  })
}

// Initialize navigation
function initializeNavigation() {
  // Smooth scrolling for anchor links
  const anchorLinks = document.querySelectorAll('a[href^="#"]')
  anchorLinks.forEach((link) => {
    link.addEventListener("click", function (e) {
      e.preventDefault()
      const targetId = this.getAttribute("href").substring(1)
      const targetElement = document.getElementById(targetId)

      if (targetElement) {
        targetElement.scrollIntoView({
          behavior: "smooth",
          block: "start",
        })
      }
    })
  })

  // Navbar scroll effect
  const navbar = document.querySelector(".custom-navbar")
  if (navbar) {
    window.addEventListener("scroll", () => {
      if (window.scrollY > 50) {
        navbar.style.background = "rgba(255, 255, 255, 0.98)"
        navbar.style.boxShadow = "0 2px 20px rgba(0, 0, 0, 0.1)"
      } else {
        navbar.style.background = "rgba(255, 255, 255, 0.95)"
        navbar.style.boxShadow = "0 2px 10px rgba(0, 0, 0, 0.1)"
      }
    })
  }
}

// Initialize copy button
function initializeCopyButton() {
  const copyBtn = document.getElementById("copyBtn")
  const shareUrl = document.getElementById("shareUrl")

  if (copyBtn && shareUrl) {
    copyBtn.addEventListener("click", function () {
      navigator.clipboard.writeText(shareUrl.value).then(() => {
        copyBtn.innerHTML = '<i class="fas fa-check"></i>'
        showSuccessMessage("URL copied successfully!")
        setTimeout(() => {
          copyBtn.innerHTML = '<i class="fas fa-copy"></i>'
        }, 2000)
      }).catch((err) => {
        console.error("Failed to copy: ", err)
        showErrorMessage("Failed to copy the URL!")
      })
    })
  } else {
    console.warn("copyBtn or shareUrl not found in the DOM")
  }
}

// Utility functions
function validateForm(form) {
  const requiredFields = form.querySelectorAll("[required]")
  let isValid = true

  requiredFields.forEach((field) => {
    if (!field.value.trim()) {
      field.classList.add("is-invalid")
      isValid = false
    } else {
      field.classList.remove("is-invalid")
      field.classList.add("is-valid")
    }
  })

  return isValid
}

function showSuccessMessage(message) {
  const successDiv = document.createElement("div")
  successDiv.className = "success-message"
  successDiv.innerHTML = `
        <i class="fas fa-check-circle me-2"></i>
        ${message}
    `

  document.body.appendChild(successDiv)

  setTimeout(() => {
    successDiv.style.animation = "slideInRight 0.3s ease-out reverse"
    setTimeout(() => {
      document.body.removeChild(successDiv)
    }, 300)
  }, 3000)
}

function showErrorMessage(message) {
  const errorDiv = document.createElement("div")
  errorDiv.className = "success-message"
  errorDiv.style.background = "var(--danger-color)"
  errorDiv.innerHTML = `
        <i class="fas fa-exclamation-circle me-2"></i>
        ${message}
    `

  document.body.appendChild(errorDiv)

  setTimeout(() => {
    errorDiv.style.animation = "slideInRight 0.3s ease-out reverse"
    setTimeout(() => {
      document.body.removeChild(errorDiv)
    }, 300)
  }, 3000)
}

// Lazy loading for images
function initializeLazyLoading() {
  const images = document.querySelectorAll("img[data-src]")

  const imageObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const img = entry.target
        img.src = img.dataset.src
        img.classList.remove("lazy")
        imageObserver.unobserve(img)
      }
    })
  })

  images.forEach((img) => imageObserver.observe(img))
}

// Initialize search functionality
function initializeSearch() {
  const searchInput = document.querySelector(".search-input")
  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      const searchTerm = e.target.value.toLowerCase()
      const posts = document.querySelectorAll(".post-card")

      posts.forEach((post) => {
        const title = post.querySelector(".post-title").textContent.toLowerCase()
        const excerpt = post.querySelector(".post-excerpt").textContent.toLowerCase()

        if (title.includes(searchTerm) || excerpt.includes(searchTerm)) {
          post.style.display = "block"
        } else {
          post.style.display = "none"
        }
      })
    })
  }
}

// Theme switcher
function initializeThemeSwitcher() {
  const themeToggle = document.querySelector(".theme-toggle")
  if (themeToggle) {
    themeToggle.addEventListener("click", () => {
      document.body.classList.toggle("dark-theme")
      localStorage.setItem("theme", document.body.classList.contains("dark-theme") ? "dark" : "light")
    })

    // Load saved theme
    const savedTheme = localStorage.getItem("theme")
    if (savedTheme === "dark") {
      document.body.classList.add("dark-theme")
    }
  }
}

// Performance optimization
window.addEventListener("load", () => {
  // Remove loading class from body
  document.body.classList.remove("loading")

  // Initialize non-critical features
  setTimeout(() => {
    initializeAnimations()
  }, 100)
})

// Error handling
window.addEventListener("error", (e) => {
  console.error("JavaScript Error:", e.error)
})

// Service Worker registration (for PWA features)
if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker
      .register("/sw.js")
      .then((registration) => {
        console.log("SW registered: ", registration)
      })
      .catch((registrationError) => {
        console.log("SW registration failed: ", registrationError)
      })
  })
}
