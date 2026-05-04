import { AbsoluteFill, staticFile, useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { Video } from "@remotion/media";
import { instrumentSerif, dmSans } from "./fonts";

interface IngredientClipProps {
  videoFile: string;
  label: string;
}

export const IngredientClip: React.FC<IngredientClipProps> = ({
  videoFile,
  label,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const labelOpacity = interpolate(frame, [0.2 * fps, 0.6 * fps], [0, 1], {
    extrapolateRight: "clamp",
  });
  const labelY = interpolate(frame, [0.2 * fps, 0.6 * fps], [15, 0], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill>
      <Video
        src={staticFile(videoFile)}
        muted
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
        }}
      />

      {/* Stronger gradient overlay at bottom */}
      <div
        style={{
          position: "absolute",
          bottom: 0,
          left: 0,
          right: 0,
          height: "40%",
          background:
            "linear-gradient(transparent, rgba(26, 24, 21, 0.9))",
        }}
      />

      {/* Ingredient label — bigger and bolder */}
      <div
        style={{
          position: "absolute",
          bottom: 70,
          left: 0,
          right: 0,
          textAlign: "center",
          fontFamily: instrumentSerif,
          fontSize: 52,
          color: "#ffffff",
          opacity: labelOpacity,
          transform: `translateY(${labelY}px)`,
          textShadow: "0 2px 20px rgba(0, 0, 0, 0.6)",
        }}
      >
        {label}
      </div>
    </AbsoluteFill>
  );
};
