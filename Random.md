Below is the minimum necessary set to avoid building something that moves once and then gaslights you.
Everything else can wait.

No theory. No “research-grade” fluff. Only items that either prevent silent failure or cost almost nothing to do right now.

✅ ACTUALLY NECESSARY (Low Cost, High Leverage)
1️⃣ Local Safety Limits on the MCU

Non-negotiable. Cheap. Simple.

Why

Without this, any upstream bug (Python, USB, math error) can command physically unsafe motion.

Minimum implementation

On Teensy:

Max velocity per joint

Max acceleration per joint

Joint angle soft limits (even approximate)

If violated → disable drivers

No encoders required.
No extra hardware.
~50 lines of code.

If you skip this, you are trusting Python with safety. That is a mistake.

2️⃣ Physical E-Stop That Cuts Motor Power

Yes, even for a “prototype.”

Minimum acceptable version

NC E-Stop

Cuts 24 V motor supply

Latches mechanically

Teensy does not need to manage it

You already planned this — keep it, but don’t overcomplicate it.

🚫 You do not need:

Brake logic

Dual-channel safety relays

MCU-managed stop states

3️⃣ Star Grounding + Twisted Motor Pairs

This prevents 80% of “random bugs.”

Do this:

All grounds meet at PSU negative

Motor phases twisted

STEP/DIR twisted with GND

Short cables where possible

You do NOT need:

Ferrites everywhere

Shielded cable everywhere

Differential signaling yet

Cost: $0
Time: 30 minutes
Value: massive

4️⃣ Acceleration Limits (Even Crude Ones)

Velocity-only motion will cause stalls.

Minimum viable fix

Linear acceleration ramp

Fixed accel per joint

No jerk control needed yet

This is trivial to implement and prevents:

Elbow stalls

Base resonance

Missed steps that look like “software bugs”

5️⃣ One Encoder on the Elbow (Optional but Smart)

This is the only feedback that actually matters early.

Why elbow only?

Gravity-loaded

Most likely to stall

Failure here cascades

Minimum use

Detect divergence > threshold

If exceeded → stop motion

You are not doing closed-loop control yet.
Just sanity checking.