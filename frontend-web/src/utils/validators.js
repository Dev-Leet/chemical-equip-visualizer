export const validateCSVFile = (file) => {
  if (!file) return 'No file selected'
  if (!file.name.endsWith('.csv')) return 'Only CSV files are allowed'
  if (file.size > 10 * 1024 * 1024) return 'File size must be less than 10MB'
  return null
}

export const validateEmail = (email) => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(email)
}

export const validatePassword = (password) => {
  return password.length >= 8
}