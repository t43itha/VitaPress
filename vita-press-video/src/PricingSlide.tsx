import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { instrumentSerif, dmSans } from "./fonts";
import { theme } from "./theme";

export const PricingSlide: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const mainOpacity = interpolate(frame, [0, 0.5 * fps], [0, 1], {
    extrapolateRight: "clamp",
  });
  const mainY = interpolate(frame, [0, 0.5 * fps], [30, 0], {
    extrapolateRight: "clamp",
  });

  const priceOpacity = interpolate(frame, [0.3 * fps, 0.7 * fps], [0, 1], {
    extrapolateRight: "clamp",
  });
  const priceScale = interpolate(frame, [0.3 * fps, 0.7 * fps], [0.9, 1], {
    extrapolateRight: "clamp",
  });

  const dealOpacity = interpolate(frame, [0.7 * fps, 1.1 * fps], [0, 1], {
    extrapolateRight: "clamp",
  });
  const dealY = interpolate(frame, [0.7 * fps, 1.1 * fps], [15, 0], {
    extrapolateRight: "clamp",
  });

  const logoOpacity = interpolate(frame, [1.2 * fps, 1.6 * fps], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: theme.bg,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      {/* Subtle accent glow */}
      <div
        style={{
          position: "absolute",
          width: 600,
          height: 600,
          borderRadius: "50%",
          background: `radial-gradient(circle, ${theme.accent} 0%, transparent 60%)`,
          opacity: 0.08,
          filter: "blur(100px)",
        }}
      />

      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 32,
        }}
      >
        {/* Single price */}
        <div
          style={{
            opacity: mainOpacity,
            transform: `translateY(${mainY}px)`,
            textAlign: "center",
          }}
        >
          <div
            style={{
              fontFamily: dmSans,
              fontSize: 20,
              fontWeight: 500,
              letterSpacing: "0.15em",
              textTransform: "uppercase" as const,
              color: "rgba(255, 255, 255, 0.5)",
              marginBottom: 16,
            }}
          >
            250ml bottle
          </div>
          <div
            style={{
              fontFamily: instrumentSerif,
              fontSize: 120,
              color: "#ffffff",
              lineHeight: 0.9,
              opacity: priceOpacity,
              transform: `scale(${priceScale})`,
            }}
          >
            £3.50
          </div>
        </div>

        {/* Divider */}
        <div
          style={{
            width: 60,
            height: 1,
            backgroundColor: "rgba(255, 255, 255, 0.15)",
            opacity: dealOpacity,
          }}
        />

        {/* Bundle deal */}
        <div
          style={{
            opacity: dealOpacity,
            transform: `translateY(${dealY}px)`,
            textAlign: "center",
          }}
        >
          <div
            style={{
              fontFamily: instrumentSerif,
              fontSize: 64,
              color: theme.accent,
              lineHeight: 1,
              textShadow: `0 4px 30px ${theme.accent}44`,
            }}
          >
            3 for £10
          </div>
          <div
            style={{
              fontFamily: dmSans,
              fontSize: 18,
              fontWeight: 400,
              color: "rgba(255, 255, 255, 0.45)",
              marginTop: 12,
              letterSpacing: "0.05em",
            }}
          >
            Mix & match any flavour
          </div>
        </div>
      </div>

      {/* Vita Press wordmark */}
      <div
        style={{
          position: "absolute",
          bottom: 32,
          right: 50,
          fontFamily: instrumentSerif,
          fontSize: 36,
          letterSpacing: "0.01em",
          color: theme.accent,
          textShadow: `0 2px 20px ${theme.accent}44`,
          opacity: logoOpacity * 0.5,
        }}
      >
        Vita Press
      </div>
    </AbsoluteFill>
  );
};
