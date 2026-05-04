import { AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { instrumentSerif, dmSans } from "./fonts";
import { theme } from "./theme";

interface JuiceTextCardProps {
  name: string;
  tagline?: string;
  ingredients: string;
  benefit: string;
  accentColor: string;
  bottleImage: string;
}

export const JuiceTextCard: React.FC<JuiceTextCardProps> = ({
  name,
  tagline,
  ingredients,
  benefit,
  accentColor,
  bottleImage,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Bottle — punchy entrance
  const bottleOpacity = interpolate(frame, [0, 0.4 * fps], [0, 1], {
    extrapolateRight: "clamp",
  });
  const bottleY = interpolate(frame, [0, 0.5 * fps], [60, 0], {
    extrapolateRight: "clamp",
  });
  const bottleScale = interpolate(frame, [0, 0.5 * fps], [0.85, 1], {
    extrapolateRight: "clamp",
  });

  // Glow builds after bottle lands
  const glowIntensity = interpolate(frame, [0.4 * fps, 1.5 * fps], [0, 1], {
    extrapolateRight: "clamp",
  });

  // Name — big entrance
  const nameOpacity = interpolate(frame, [0.3 * fps, 0.65 * fps], [0, 1], {
    extrapolateRight: "clamp",
  });
  const nameY = interpolate(frame, [0.3 * fps, 0.65 * fps], [30, 0], {
    extrapolateRight: "clamp",
  });
  const nameScale = interpolate(frame, [0.3 * fps, 0.65 * fps], [0.9, 1], {
    extrapolateRight: "clamp",
  });

  // Tagline under name
  const tagOpacity = interpolate(frame, [0.55 * fps, 0.9 * fps], [0, 1], {
    extrapolateRight: "clamp",
  });

  // Ingredients
  const ingredientsOpacity = interpolate(
    frame,
    [0.7 * fps, 1.05 * fps],
    [0, 1],
    { extrapolateRight: "clamp" }
  );

  // Divider
  const dividerWidth = interpolate(frame, [0.9 * fps, 1.2 * fps], [0, 50], {
    extrapolateRight: "clamp",
  });

  // Benefit
  const benefitOpacity = interpolate(
    frame,
    [1.0 * fps, 1.4 * fps],
    [0, 1],
    { extrapolateRight: "clamp" }
  );
  const benefitY = interpolate(frame, [1.0 * fps, 1.4 * fps], [15, 0], {
    extrapolateRight: "clamp",
  });

  // Trust badges — staggered
  const trustBadges = [
    { icon: "✓", label: "No Additives" },
    { icon: "✓", label: "No Added Sugar" },
    { icon: "✓", label: "Freshly Pressed" },
    { icon: "✓", label: "No Compromise" },
  ];
  const badgeDelay = (i: number) => (1.3 + i * 0.15) * fps;
  const badgeOpacity = (i: number) =>
    interpolate(frame, [badgeDelay(i), badgeDelay(i) + 0.3 * fps], [0, 1], {
      extrapolateRight: "clamp",
    });
  const badgeScale = (i: number) =>
    interpolate(frame, [badgeDelay(i), badgeDelay(i) + 0.3 * fps], [0.85, 1], {
      extrapolateRight: "clamp",
    });

  return (
    <AbsoluteFill style={{ backgroundColor: theme.bg }}>
      {/* Large ambient glow — fills left side */}
      <div
        style={{
          position: "absolute",
          left: "-5%",
          top: "0%",
          width: 900,
          height: 900,
          borderRadius: "50%",
          background: `radial-gradient(circle, ${accentColor} 0%, transparent 60%)`,
          opacity: glowIntensity * 0.18,
          filter: "blur(100px)",
        }}
      />

      {/* Floor reflection glow */}
      <div
        style={{
          position: "absolute",
          left: "10%",
          bottom: "-10%",
          width: 600,
          height: 300,
          borderRadius: "50%",
          background: `radial-gradient(ellipse, ${accentColor} 0%, transparent 70%)`,
          opacity: glowIntensity * 0.12,
          filter: "blur(60px)",
        }}
      />

      {/* Right side subtle accent glow */}
      <div
        style={{
          position: "absolute",
          right: "5%",
          top: "30%",
          width: 400,
          height: 400,
          borderRadius: "50%",
          background: `radial-gradient(circle, ${accentColor} 0%, transparent 70%)`,
          opacity: glowIntensity * 0.06,
          filter: "blur(80px)",
        }}
      />

      {/* Left: Bottle — large and dominant */}
      <div
        style={{
          position: "absolute",
          left: 0,
          top: 0,
          bottom: 0,
          width: "46%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          opacity: bottleOpacity,
          transform: `translateY(${bottleY}px) scale(${bottleScale})`,
        }}
      >
        <Img
          src={staticFile(bottleImage)}
          style={{
            height: 850,
            objectFit: "contain",
            filter: `drop-shadow(0 40px 100px ${accentColor}40) drop-shadow(0 10px 30px rgba(0,0,0,0.6))`,
          }}
        />
      </div>

      {/* Right: Text content */}
      <div
        style={{
          position: "absolute",
          right: 0,
          top: 0,
          bottom: 0,
          width: "50%",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          paddingRight: 90,
          gap: 20,
        }}
      >
        {/* Juice name — massive, the hero */}
        <div
          style={{
            fontFamily: instrumentSerif,
            fontSize: 130,
            letterSpacing: "-0.03em",
            color: accentColor,
            lineHeight: 0.9,
            opacity: nameOpacity,
            transform: `translateY(${nameY}px) scale(${nameScale})`,
            textShadow: `0 6px 40px ${accentColor}44`,
          }}
        >
          {name}
        </div>

        {/* Sub-tagline */}
        <div
          style={{
            fontFamily: dmSans,
            fontSize: 18,
            fontWeight: 600,
            letterSpacing: "0.2em",
            textTransform: "uppercase" as const,
            color: accentColor,
            opacity: tagOpacity * 0.7,
            marginTop: -4,
          }}
        >
          {tagline}
        </div>

        {/* Ingredients */}
        <div
          style={{
            fontFamily: dmSans,
            fontSize: 20,
            fontWeight: 400,
            letterSpacing: "0.18em",
            textTransform: "uppercase" as const,
            color: "rgba(255, 255, 255, 0.45)",
            opacity: ingredientsOpacity,
            marginTop: 8,
          }}
        >
          {ingredients}
        </div>

        {/* Divider — animated width */}
        <div
          style={{
            width: dividerWidth,
            height: 1,
            backgroundColor: "rgba(255, 255, 255, 0.12)",
            marginTop: 4,
            marginBottom: 4,
          }}
        />

        {/* Benefit — bold, white, the sell */}
        <div
          style={{
            fontFamily: dmSans,
            fontSize: 32,
            fontWeight: 400,
            lineHeight: 1.65,
            color: "#ffffff",
            opacity: benefitOpacity,
            transform: `translateY(${benefitY}px)`,
            maxWidth: 500,
          }}
        >
          {benefit}
        </div>

        {/* Trust badges — 2x2 grid, minimal and big */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1fr 1fr",
            columnGap: 0,
            rowGap: 20,
            marginTop: 16,
          }}
        >
          {trustBadges.map((badge, i) => (
            <div
              key={badge.label}
              style={{
                display: "flex",
                alignItems: "center",
                gap: 16,
                opacity: badgeOpacity(i),
                transform: `scale(${badgeScale(i)})`,
              }}
            >
              {/* Checkmark circle */}
              <div
                style={{
                  width: 40,
                  height: 40,
                  borderRadius: "50%",
                  border: `2px solid ${accentColor}`,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontSize: 18,
                  fontWeight: 700,
                  color: accentColor,
                  flexShrink: 0,
                }}
              >
                ✓
              </div>
              <div
                style={{
                  fontFamily: dmSans,
                  fontSize: 18,
                  fontWeight: 500,
                  letterSpacing: "0.02em",
                  color: "rgba(255, 255, 255, 0.85)",
                }}
              >
                {badge.label}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Vita Press wordmark — anchored bottom-right */}
      <div
        style={{
          position: "absolute",
          bottom: 30,
          right: 50,
          fontFamily: instrumentSerif,
          fontSize: 36,
          letterSpacing: "0.01em",
          color: theme.accent,
          textShadow: `0 2px 20px ${theme.accent}44`,
          opacity: benefitOpacity,
        }}
      >
        Vita Press
      </div>
    </AbsoluteFill>
  );
};
