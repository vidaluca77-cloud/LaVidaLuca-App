export default function Home() {
  return (
    <div className="font-sans grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20">
      <main className="flex flex-col gap-[32px] row-start-2 items-center sm:items-start max-w-2xl text-center sm:text-left">
        <h1 className="text-4xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-6xl">
          La Vida Luca
        </h1>
        
        <p className="text-lg text-gray-600 dark:text-gray-300 leading-relaxed">
          Plateforme collaborative d'apprentissage dédiée à la formation des jeunes 
          en Maisons Familiales Rurales et au développement de nouvelles pratiques agricoles.
        </p>

        <div className="flex gap-4 items-center flex-col sm:flex-row">
          <a
            className="rounded-full border border-solid border-transparent transition-colors flex items-center justify-center bg-blue-600 text-white gap-2 hover:bg-blue-700 font-medium text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5"
            href="/activites"
          >
            Explorer les activités
          </a>
          <a
            className="rounded-full border border-solid border-blue-600 text-blue-600 transition-colors flex items-center justify-center hover:bg-blue-50 dark:hover:bg-blue-900/20 font-medium text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5"
            href="/proposer-aide"
          >
            Proposer de l'aide
          </a>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 mt-8 w-full">
          <div className="text-center p-4">
            <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Collaboration</h3>
            <p className="text-sm text-gray-600 dark:text-gray-300">
              Connectez-vous avec d'autres étudiants et partagez vos expériences
            </p>
          </div>
          <div className="text-center p-4">
            <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Agriculture Moderne</h3>
            <p className="text-sm text-gray-600 dark:text-gray-300">
              Découvrez les nouvelles pratiques agricoles durables
            </p>
          </div>
          <div className="text-center p-4">
            <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Formation</h3>
            <p className="text-sm text-gray-600 dark:text-gray-300">
              Accédez à des ressources pédagogiques adaptées aux MFR
            </p>
          </div>
        </div>
      </main>
      
      <footer className="row-start-3 flex gap-[24px] flex-wrap items-center justify-center text-sm text-gray-500">
        <a
          className="hover:underline hover:underline-offset-4"
          href="/test-ia"
        >
          Assistant IA
        </a>
        <a
          className="hover:underline hover:underline-offset-4"
          href="mailto:contact@lavidaluca.fr"
        >
          Contact
        </a>
        <span>© 2024 La Vida Luca</span>
      </footer>
    </div>
  );
}
