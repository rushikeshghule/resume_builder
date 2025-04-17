// ResumeCraft JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Template selection handling
    const templateCards = document.querySelectorAll('.template-card');
    const templateInput = document.getElementById('id_template');
    
    if (templateCards.length > 0 && templateInput) {
        templateCards.forEach(card => {
            card.addEventListener('click', function() {
                // Clear previous selection
                templateCards.forEach(c => c.classList.remove('selected'));
                
                // Select this card
                this.classList.add('selected');
                
                // Update hidden input
                templateInput.value = this.dataset.templateId;
            });
        });
    }
    
    // Current employment/education checkbox handling
    const currentCheckboxes = document.querySelectorAll('.is-current-checkbox');
    
    if (currentCheckboxes.length > 0) {
        currentCheckboxes.forEach(checkbox => {
            const endDateField = checkbox.closest('.form-row').querySelector('.end-date-field');
            
            // Initial state
            if (checkbox.checked) {
                endDateField.style.display = 'none';
            }
            
            // Change event
            checkbox.addEventListener('change', function() {
                if (this.checked) {
                    endDateField.style.display = 'none';
                } else {
                    endDateField.style.display = 'block';
                }
            });
        });
    }
    
    // FormSet handling - add more buttons
    const addButtons = document.querySelectorAll('.add-form-row');
    
    if (addButtons.length > 0) {
        addButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                
                const formsetName = this.dataset.formset;
                const totalFormsInput = document.getElementById(`id_${formsetName}-TOTAL_FORMS`);
                const formsetContainer = document.getElementById(`${formsetName}-formset`);
                
                // Get current form count
                let formCount = parseInt(totalFormsInput.value);
                
                // Clone the empty form template
                const emptyFormElement = document.getElementById(`empty-${formsetName}-form`);
                const emptyFormHTML = emptyFormElement.innerHTML.replace(/__prefix__/g, formCount);
                
                // Create a new form element
                const formRow = document.createElement('div');
                formRow.classList.add('form-row', 'mb-4', 'border-bottom', 'pb-4');
                formRow.innerHTML = emptyFormHTML;
                
                // Add the new form to the container
                formsetContainer.appendChild(formRow);
                
                // Update form count
                totalFormsInput.value = formCount + 1;
                
                // Initialize any JS for the new form elements
                initializeFormElements(formRow);
            });
        });
    }
    
    // Initialize date pickers and other form elements
    function initializeFormElements(container) {
        // Initialize any new date pickers or other special form elements
        const currentCheckboxes = container.querySelectorAll('.is-current-checkbox');
        
        if (currentCheckboxes.length > 0) {
            currentCheckboxes.forEach(checkbox => {
                const endDateField = checkbox.closest('.form-row').querySelector('.end-date-field');
                
                // Initial state
                if (checkbox.checked) {
                    endDateField.style.display = 'none';
                }
                
                // Change event
                checkbox.addEventListener('change', function() {
                    if (this.checked) {
                        endDateField.style.display = 'none';
                    } else {
                        endDateField.style.display = 'block';
                    }
                });
            });
        }
    }
    
    // Live preview updates
    const previewFrame = document.getElementById('resume-preview-frame');
    const resumeForm = document.getElementById('resume-form');
    
    if (previewFrame && resumeForm) {
        const formInputs = resumeForm.querySelectorAll('input, textarea, select');
        
        formInputs.forEach(input => {
            input.addEventListener('change', updatePreview);
            input.addEventListener('keyup', debounce(updatePreview, 500));
        });
        
        function updatePreview() {
            // Send form data to preview endpoint via fetch
            const formData = new FormData(resumeForm);
            
            fetch('/resume/preview-update/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.text())
            .then(html => {
                // Update the preview iframe
                const doc = previewFrame.contentDocument;
                doc.open();
                doc.write(html);
                doc.close();
            })
            .catch(error => {
                console.error('Error updating preview:', error);
            });
        }
    }
    
    // Resume visibility toggle
    const visibilityToggles = document.querySelectorAll('.visibility-toggle');
    
    if (visibilityToggles.length > 0) {
        visibilityToggles.forEach(toggle => {
            toggle.addEventListener('click', function(e) {
                e.preventDefault();
                
                const resumeId = this.dataset.resumeSlug;
                const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
                
                fetch(`/resume/${resumeId}/toggle-visibility/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        // Update the UI based on visibility
                        const icon = this.querySelector('i');
                        const text = this.querySelector('span');
                        
                        if (data.is_public) {
                            icon.classList.remove('fa-eye-slash');
                            icon.classList.add('fa-eye');
                            text.textContent = 'Public';
                            this.classList.remove('btn-secondary');
                            this.classList.add('btn-success');
                        } else {
                            icon.classList.remove('fa-eye');
                            icon.classList.add('fa-eye-slash');
                            text.textContent = 'Private';
                            this.classList.remove('btn-success');
                            this.classList.add('btn-secondary');
                        }
                    }
                })
                .catch(error => {
                    console.error('Error toggling visibility:', error);
                });
            });
        });
    }
    
    // Helper function for debouncing
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
});
