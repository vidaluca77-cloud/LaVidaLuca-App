import type { Metadata } from "next";
import AgriAssistant from "@/components/AgriAssistant";

export const metadata: Metadata = {
  title: "Assistant Agricole IA",
  description: "Obtenez des conseils agricoles personnalisés grâce à notre assistant IA spécialisé en agriculture durable et permaculture.",
};

export default function AssistantPage() {
  return (
    <div className="space-y-6">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          Assistant Agricole Intelligent
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Posez vos questions sur l'agriculture, le jardinage, la permaculture et obtenez des conseils 
          personnalisés basés sur les meilleures pratiques durables.
        </p>
      </div>
      
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h3 className="font-semibold text-blue-900 mb-2">💡 Exemples de questions :</h3>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• "Comment améliorer un sol argileux compact ?"</li>
          <li>• "Que planter en ce moment dans ma région ?"</li>
          <li>• "Comment traiter naturellement les pucerons ?"</li>
          <li>• "Quand et comment faire son compost ?"</li>
        </ul>
      </div>

      <AgriAssistant />
    </div>
  );
}