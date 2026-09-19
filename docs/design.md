# Design Spec

## Information architecture

**Left:** conversation and model/mode controls.

**Right:** artifact viewer.

This keeps reasoning and generated output visible at the same time.

## Interaction states

1. Empty state — explain what the assistant can answer.
2. Retrieving — gather transcript evidence.
3. Answering — stream or display grounded response.
4. Sources — expandable evidence.
5. Artifact — render Markdown or HTML separately.
6. Failure — explain whether the problem is retrieval, model, or configuration.

## Responsive behavior

- Desktop: two-column chat + artifact layout.
- Narrow screens: stack chat above artifact.
- Source evidence stays collapsible to reduce cognitive load.

## Accessibility

- Native Streamlit controls.
- Clear labels for model and mode.
- High-contrast text.
- Avoid information being conveyed only by color.
- Artifact content has a visible title and separate boundary.

## Design decision

The interface prioritizes evaluator comprehension: they can immediately see the question, retrieved evidence, model provider, and generated artifact without leaving the page.
