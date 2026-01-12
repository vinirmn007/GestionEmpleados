import { writable } from 'svelte/store';
import { browser } from '$app/environment';

const defaultSettings = {
    fontSize: 'normal', // 'normal', 'large', 'xlarge'
    highContrast: false,
    reducedMotion: false,
    underlineLinks: false
};

const storedSettings = browser ? JSON.parse(localStorage.getItem('accessibility') || 'null') : null;

export const accessibility = writable(storedSettings || defaultSettings);

accessibility.subscribe((value) => {
    if (browser) {
        localStorage.setItem('accessibility', JSON.stringify(value));

        // Apply font size
        document.documentElement.classList.remove('text-normal', 'text-large', 'text-xlarge');
        document.documentElement.classList.add(`text-${value.fontSize}`);

        // Apply high contrast
        if (value.highContrast) {
            document.documentElement.classList.add('high-contrast');
        } else {
            document.documentElement.classList.remove('high-contrast');
        }

        // Apply reduced motion
        if (value.reducedMotion) {
            document.documentElement.classList.add('reduce-motion');
        } else {
            document.documentElement.classList.remove('reduce-motion');
        }

        // Apply underline links
        if (value.underlineLinks) {
            document.documentElement.classList.add('underline-links');
        } else {
            document.documentElement.classList.remove('underline-links');
        }
    }
});

export function setFontSize(size) {
    accessibility.update(a => ({ ...a, fontSize: size }));
}

export function toggleHighContrast() {
    accessibility.update(a => ({ ...a, highContrast: !a.highContrast }));
}

export function toggleReducedMotion() {
    accessibility.update(a => ({ ...a, reducedMotion: !a.reducedMotion }));
}

export function toggleUnderlineLinks() {
    accessibility.update(a => ({ ...a, underlineLinks: !a.underlineLinks }));
}

export function resetAccessibility() {
    accessibility.set(defaultSettings);
}
