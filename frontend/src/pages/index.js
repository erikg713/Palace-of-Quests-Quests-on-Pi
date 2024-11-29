import Layout from '../components/layout'
import NestedLayout from '../components/nested-layout'
 
const Page = () => {
  return <p>hello world</p>
}
 
Page.getLayout = function getLayout(page) {
  return (
    <Layout>
      <NestedLayout>{page}</NestedLayout>
    </Layout>
  )
}
 
export default Page