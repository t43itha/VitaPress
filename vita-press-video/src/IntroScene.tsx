import { AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { instrumentSerif, dmSans } from "./fonts";
import { theme } from "./theme";

export const IntroScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const wordmarkOpacity = interpolate(frame, [0, 1 * fps], [0, 1], {
    extrapolateRight: "clamp",
  });
  const wordmarkY = interpolate(frame, [0, 1 * fps], [40, 0], {
    extrapolateRight: "clamp",
  });
  const wordmarkScale = interpolate(frame, [0, 1 * fps], [0.9, 1], {
    extrapolateRight: "clamp",
  });

  const taglineOpacity = interpolate(
    frame,
    [0.8 * fps, 1.6 * fps],
    [0, 1],
    { extrapolateRight: "clamp" }
  );
  const taglineY = interpolate(frame, [0.8 * fps, 1.6 * fps], [25, 0], {
    extrapolateRight: "clamp",
  });

  // Slow zoom on background photo
  const bgScale = interpolate(frame, [0, 5 * fps], [1, 1.08], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill>
      {/* Background photo with slow zoom */}
      <div
        style={{
          width: "100%",
          height: "100%",
          transform: `scale(${bgScale})`,
          overflow: "hidden",
        }}
      >
        <Img
          src={staticFile("market-stall-bg.jpg")}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
          }}
        />
      </div>

      {/* Darker overlay for better contrast */}
      <AbsoluteFill
        style={{ backgroundColor: "rgba(26, 24, 21, 0.7)" }}
      />

      {/* Content */}
      <AbsoluteFill
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          gap: 32,
        }}
      >
        <div
          style={{
            fontFamily: instrumentSerif,
            fontSize: 140,
            letterSpacing: "-0.03em",
            color: theme.accent,
            opacity: wordmarkOpacity,
            transform: `translateY(${wordmarkY}px) scale(${wordmarkScale})`,
            textShadow: "0 4px 30px rgba(212, 112, 10, 0.4)",
          }}
        >
          Vita Press
        </div>
        <div
          style={{
            fontFamily: dmSans,
            fontSize: 36,
            fontWeight: 400,
            color: "#ffffff",
            letterSpacing: "0.06em",
            textTransform: "uppercase" as const,
            opacity: taglineOpacity,
            transform: `translateY(${taglineY}px)`,
          }}
        >
          Fresh-pressed. No additives. No compromise.
        </div>
      </AbsoluteFill>

      {/* Footer */}
      <div
        style={{
          position: "absolute",
          bottom: 40,
          right: 60,
          fontFamily: dmSans,
          fontSize: 14,
          fontWeight: 500,
          letterSpacing: "0.12em",
          textTransform: "uppercase" as const,
          color: theme.textMuted,
          opacity: taglineOpacity,
        }}
      >
        Fresh-pressed · No additives · No compromise
      </div>
    </AbsoluteFill>
  );
};
