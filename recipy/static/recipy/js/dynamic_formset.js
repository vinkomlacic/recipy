// Closure - no need to expose any of these functions globally.
(() => {
    /**
     * Button which adds another form to a formset when clicked.
     *
     * To use this class you need to set several data attributes on this element:
     *  - data-formset: selector of the formset container (div normally)
     *  - data-formset-prefix: prefix of the formset (tip: use formset.prefix to
     *      get this value in the Django template)
     *  - data-empty-form: selector of the form used for duplicating and creating new form
     *      (tip: use formset.empty_form to generate this form and place outside the form)
     */
    $('.formset-add-more-btn').click(function (e) {
        const button = $(e.target);

        const formsetSelector = getDataAttributeOrThrowError(button, 'formset');
        const emptyFormSelector = getDataAttributeOrThrowError(button, 'empty-form');
        const formsetPrefix = getDataAttributeOrThrowError(button, 'formset-prefix');

        addFormToFormset(formsetSelector, emptyFormSelector, formsetPrefix)
    });

    function addFormToFormset(formsetSelector, emptyFormSelector, formsetPrefix) {
        const totalForms = getElementOrThrowError(`#id_${formsetPrefix}-TOTAL_FORMS`);
        const totalFormsCount = totalForms.val();

        const formset = getElementOrThrowError(formsetSelector);
        // New form ID is equal to the current number of forms in the formset
        const newFormHtml = createNewFormHtml(emptyFormSelector, totalFormsCount);
        formset.append(newFormHtml);

        // Increment the current number of forms in the formset
        totalForms.val(parseInt(totalFormsCount) + 1);
    }

    function createNewFormHtml(emptyFormSelector, newFormId) {
        const emptyForm = getElementOrThrowError(emptyFormSelector);
        const emptyFormHtml = emptyForm.html();
        return emptyFormHtml.replace(/__prefix__/g, newFormId);
    }

    function getDataAttributeOrThrowError(element, key) {
        const attributeName = `data-${key}`;
        const value = element.attr(attributeName);
        if (!value) {
            const msg = `${attributeName} not set on the element!`;
            throw new Error(msg);
        }

        return value
    }

    function getElementOrThrowError(selector) {
        const element = $(selector);
        if (!element.length) {
            const msg = `Element specified with the selector "${selector}" does not exist.`;
            throw new Error(msg);
        }

        return element;
    }
})();
