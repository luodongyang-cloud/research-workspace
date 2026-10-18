# Layered Fig. 1 draft

Conceptual functional layers, not a physical 3D stack. Spatial layer order does not establish sensing/write chronology or validated parallel operation. The same selected sensor is used by the single-pixel inset; no extra S is drawn in the circuit layer. TG1 connects V_in to the capacitor node; C connects that node to reference ground; TG2 connects it to the selected S in the sensor layer, whose read current enters a virtual-ground summation interface. Rest-of-array icons are intentionally abstract.

Light history establishes volatile G; capacitor voltage V_C provides a distinct electrical state. Weight writing uses fixed V_in and variable TG1 on duration. Readout assumes approximately ohmic behavior, small switch drops and negligible capacitor droop over short pulses. Signed capacitor weights are shown conceptually as requested; right-hand traces illustrate positive read voltages only. Implementation of negative voltages requires author confirmation.

Classification uses separate scalar currents from successive weight templates. The score-card geometry is illustrative, uncalibrated and contains no measured values. G is an internal state, not an already digitized readout image. Pixel count is conceptual.

All four traces are generated from one arbitrary accumulation/decay model. Four identical optical pulses occur in sensing; G rises during pulses and continuously decays in dark. Three read-voltage pulses occur after the last optical pulse; current is the pointwise product of G and voltage. No measured performance, energy or accuracy is implied.

SVG uses editable text and grouped vector shapes. Fonts: DejaVu Sans, with Arial/sans-serif fallback. No image model or third-party generated component was used. Perspective conveys functional separation, as explicitly requested, rather than device fabrication geometry. Red/blue/white denote signed electrical weights as explicitly requested. Publication eligibility and scientific interpretation require author review.

## Caption
(a) Functional layers for optical-history encoding, capacitor weight storage, current summation and template-based classification in a GaON/GaN photomemristive 2TG1C1S array. Optical input produces volatile conductance G at zero externally applied sensor bias. TG1 writes capacitor voltage V_C; TG2 applies it to the same sensor during readout. Each template produces one scalar summed current; successive templates support classification. (b) Shared-time schematic responses: optical pulses, conductance, sensor read voltage and read current.
