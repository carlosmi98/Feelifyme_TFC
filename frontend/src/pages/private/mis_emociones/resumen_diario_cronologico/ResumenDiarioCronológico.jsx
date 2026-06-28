import { useDocumentTitle } from "../../../../hooks/useDocumentTitle"
import { ResumenCronologico } from "./components/ResumenCronologico"


export const ResumenDiarioCronológico = () => {
    useDocumentTitle('Resumen Diario');
    return (
        <ResumenCronologico />
    )
}

